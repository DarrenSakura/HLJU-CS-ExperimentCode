import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class DescSortClean {

    public static class TokenizerMapper
            extends Mapper<LongWritable, Text, IntWritable, IntWritable> {

        private IntWritable number = new IntWritable();
        private final static IntWritable one = new IntWritable(1);

        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            String line = value.toString().trim();
            if (!line.isEmpty()) {
                number.set(Integer.parseInt(line));
                context.write(number, one);
            }
        }
    }

    public static class CleanReducer
            extends Reducer<IntWritable, IntWritable, IntWritable, NullWritable> {

        public void reduce(IntWritable key, Iterable<IntWritable> values,
                           Context context) throws IOException, InterruptedException {
            context.write(key, NullWritable.get());
        }
    }

    public static class DescComparator extends WritableComparator {

        protected DescComparator() {
            super(IntWritable.class, true);
        }

        @Override
        public int compare(WritableComparable w1, WritableComparable w2) {
            IntWritable k1 = (IntWritable) w1;
            IntWritable k2 = (IntWritable) w2;
            return -k1.compareTo(k2);  // 降序
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "DescSortClean");

        job.setJarByClass(DescSortClean.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(CleanReducer.class);

        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(IntWritable.class);

        job.setSortComparatorClass(DescComparator.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
