import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MovieCount {

    public static class MCMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private Text movie = new Text();
        private final static IntWritable one = new IntWritable(1);

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString().trim();
            if (line.isEmpty()) return;

            // Skip comments and CSV header
            if (line.startsWith("#") || line.startsWith("userId")) return;

            // Split CSV by comma
            String[] parts = line.split(",");

            // Need at least userId,movieId
            if (parts.length < 2) return;

            // movieId is the second column
            movie.set(parts[1].trim());

            context.write(movie, one);
        }
    }

    public static class MCReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable out = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable v : values) sum += v.get();
            out.set(sum);
            context.write(key, out);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "MovieCount");

        job.setJarByClass(MovieCount.class);
        job.setMapperClass(MCMapper.class);
        job.setReducerClass(MCReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
