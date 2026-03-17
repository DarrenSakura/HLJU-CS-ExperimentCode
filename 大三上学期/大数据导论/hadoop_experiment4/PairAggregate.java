import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringJoiner;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class PairAggregate {

    // Identity mapper (input is pair \t user)
    public static class PAMapper extends Mapper<Object, Text, Text, Text> {
        private Text pair = new Text();
        private Text user = new Text();
        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            String line = value.toString().trim();
            if (line.isEmpty()) return;
            String[] kv = line.split("\\t");
            if (kv.length < 2) return;
            pair.set(kv[0]);
            user.set(kv[1]);
            context.write(pair, user);
        }
    }

    public static class PAReducer extends Reducer<Text, Text, Text, Text> {
        private Text outVal = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            List<String> users = new ArrayList<>();
            for (Text v : values) users.add(v.toString());
            // build comma-separated user list and output count
            StringJoiner sj = new StringJoiner(",");
            for (String u : users) sj.add(u);
            String out = users.size() + "\t" + sj.toString();
            outVal.set(out);
            context.write(key, outVal); // key: movieA,movieB ; val: coCount \t user1,user2,...
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "PairAggregate");
        job.setJarByClass(PairAggregate.class);
        job.setMapperClass(PAMapper.class);
        job.setReducerClass(PAReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
