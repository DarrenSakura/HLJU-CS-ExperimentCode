import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class UserPairs {
    public static class UPMapper extends Mapper<Object, Text, Text, Text> {
        private Text user = new Text();
        private Text movie = new Text();

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            String line = value.toString().trim();
            if (line.isEmpty()) return;
            
            // Skip comments and header
            if (line.startsWith("#") || line.startsWith("userId")) return;
            
            // Split CSV by comma
            String[] parts = line.split(",");
            if (parts.length < 2) return;
            
            // Extract userId and movieId
            user.set(parts[0].trim());
            movie.set(parts[1].trim());
            context.write(user, movie);
        }
    }

    public static class UPReducer extends Reducer<Text, Text, Text, Text> {
        private Text pair = new Text();
        private Text userOut = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            List<String> movies = new ArrayList<>();
            for (Text v : values) {
                movies.add(v.toString());
            }
            
            // Remove duplicates and sort
            Collections.sort(movies);
            
            // Generate all pairs i<j
            int n = movies.size();
            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    String a = movies.get(i);
                    String b = movies.get(j);
                    String p = a + "," + b;
                    pair.set(p);
                    userOut.set(key.toString());
                    context.write(pair, userOut);
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "UserPairs");
        job.setJarByClass(UserPairs.class);
        job.setMapperClass(UPMapper.class);
        job.setReducerClass(UPReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
