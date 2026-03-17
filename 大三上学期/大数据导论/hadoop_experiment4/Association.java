import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.DecimalFormat;
import java.util.HashMap;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Association {

    public static class AssocMapper extends Mapper<Object, Text, Text, Text> {
        private HashMap<String, Integer> movieCount = new HashMap<>();
        private DecimalFormat df = new DecimalFormat("#.####");
        private Text outKey = new Text();
        private Text outVal = new Text();

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            // 直接从HDFS读取movie_counts文件
            Configuration conf = context.getConfiguration();
            String movieCountPath = conf.get("movie.count.path", "/output/movie_counts/part-r-00000");
            
            try {
                FileSystem fs = FileSystem.get(conf);
                Path path = new Path(movieCountPath);
                BufferedReader br = new BufferedReader(new InputStreamReader(fs.open(path)));
                String line;
                while ((line = br.readLine()) != null) {
                    line = line.trim();
                    if (line.isEmpty()) continue;
                    String[] kv = line.split("\\t");
                    if (kv.length < 2) continue;
                    movieCount.put(kv[0], Integer.parseInt(kv[1]));
                }
                br.close();
                System.err.println("Loaded " + movieCount.size() + " movie counts");
            } catch (Exception e) {
                System.err.println("Error loading movie_counts: " + e.getMessage());
                e.printStackTrace();
            }
        }

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            // Input: pair \t count \t user1,user2,...
            String line = value.toString().trim();
            if (line.isEmpty()) return;
            String[] parts = line.split("\\t");
            if (parts.length < 2) return;
            String pair = parts[0];
            int coCount = Integer.parseInt(parts[1]);
            String[] movies = pair.split(",");
            if (movies.length != 2) return;
            String a = movies[0];
            String b = movies[1];
            Integer ca = movieCount.get(a);
            Integer cb = movieCount.get(b);
            if (ca == null || cb == null) {
                System.err.println("Missing count for movies: " + a + " or " + b);
                return;
            }
            double jaccard = 0.0;
            int denom = ca + cb - coCount;
            if (denom > 0) jaccard = (double) coCount / denom;
            String val = coCount + "\t" + df.format(jaccard);
            outKey.set(pair);
            outVal.set(val);
            context.write(outKey, outVal);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        
        // 可选：通过命令行参数指定movie_counts路径
        // 默认使用 /output/movie_counts/part-r-00000
        if (args.length > 2) {
            conf.set("movie.count.path", args[2]);
        }
        
        Job job = Job.getInstance(conf, "Association");
        job.setJarByClass(Association.class);
        job.setMapperClass(AssocMapper.class);
        job.setNumReduceTasks(0); // map-only
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
