import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SortByCount {

    public static class SwapMapper
         extends Mapper<Object, Text, IntWritable, Text> {

        private IntWritable freq = new IntWritable();
        private Text word = new Text();

        public void map(Object key, Text value, Context context
                        ) throws IOException, InterruptedException {
            String[] parts = value.toString().trim().split("\\s+");
            if (parts.length == 2) {
                word.set(parts[0]);
                freq.set(Integer.parseInt(parts[1]));
                context.write(freq, word);
            }
        }
    }

    // 降序排序
    public static class IntWritableDecreasingComparator
         extends WritableComparator {
        protected IntWritableDecreasingComparator() {
            super(IntWritable.class, true);
        }
        @SuppressWarnings("rawtypes")
        @Override
        public int compare(WritableComparable a, WritableComparable b) {
            return -super.compare(a, b); // 倒序
        }
    }

    public static class OutputReducer
         extends Reducer<IntWritable, Text, Text, IntWritable> {

        int count = 0;

        public void reduce(IntWritable key, Iterable<Text> values,
                           Context context
                           ) throws IOException, InterruptedException {
            for (Text word : values) {
                if (count < 10) {
                    context.write(word, key);
                    count++;
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "sort by count");
        job.setJarByClass(SortByCount.class);
        job.setMapperClass(SwapMapper.class);
        job.setReducerClass(OutputReducer.class);
        job.setSortComparatorClass(IntWritableDecreasingComparator.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
