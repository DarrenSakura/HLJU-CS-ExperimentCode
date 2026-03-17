import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

import javax.swing.JFrame;
import javax.swing.JPanel;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.RenderingHints;

public class KNNProject {

    // ==========================================
    // 基础数据结构
    // ==========================================
    static class Instance {
        double[] features;
        String label;

        public Instance(double[] features, String label) {
            this.features = features;
            this.label = label;
        }
    }

    // ==========================================
    // 步骤1：数据预处理 (标准化)
    // ==========================================
    static class StandardScaler {
        double[] mean;
        double[] std;

        public void fit(List<Instance> trainData) {
            if (trainData.isEmpty()) return;
            int numFeatures = trainData.get(0).features.length;
            mean = new double[numFeatures];
            std = new double[numFeatures];

            for (Instance inst : trainData) {
                for (int i = 0; i < numFeatures; i++) mean[i] += inst.features[i];
            }
            for (int i = 0; i < numFeatures; i++) mean[i] /= trainData.size();

            for (Instance inst : trainData) {
                for (int i = 0; i < numFeatures; i++) std[i] += Math.pow(inst.features[i] - mean[i], 2);
            }
            for (int i = 0; i < numFeatures; i++) {
                std[i] = Math.sqrt(std[i] / trainData.size());
                if (std[i] == 0) std[i] = 1.0; 
            }
        }

        public Instance transform(Instance inst) {
            double[] scaledFeatures = new double[inst.features.length];
            for (int i = 0; i < inst.features.length; i++) {
                scaledFeatures[i] = (inst.features[i] - mean[i]) / std[i];
            }
            return new Instance(scaledFeatures, inst.label);
        }

        public List<Instance> transform(List<Instance> data) {
            List<Instance> scaledData = new ArrayList<>();
            // 明确调用当前类的 transform(Instance) 方法
            for (Instance inst : data) scaledData.add(this.transform(inst));
            return scaledData;
        }
    }

    // ==========================================
    // 步骤2：实现 KNN 算法
    // ==========================================
    static class KNNClassifier {
        private int k;
        private List<Instance> trainData;

        public KNNClassifier(int k) { this.k = k; }
        public void fit(List<Instance> trainData) { this.trainData = trainData; }

        private double euclideanDistance(double[] f1, double[] f2) {
            double sum = 0.0;
            for (int i = 0; i < f1.length; i++) sum += Math.pow(f1[i] - f2[i], 2);
            return Math.sqrt(sum);
        }

        public String predict(Instance testInstance) {
            List<DistanceRecord> distances = new ArrayList<>();
            for (Instance trainInstance : trainData) {
                distances.add(new DistanceRecord(trainInstance, euclideanDistance(testInstance.features, trainInstance.features)));
            }
            distances.sort(Comparator.comparingDouble(d -> d.distance));

            Map<String, Integer> votes = new HashMap<>();
            for (int i = 0; i < Math.min(k, distances.size()); i++) {
                String label = distances.get(i).instance.label;
                votes.put(label, votes.getOrDefault(label, 0) + 1);
            }

            String bestLabel = null;
            int maxVotes = -1;
            for (Map.Entry<String, Integer> entry : votes.entrySet()) {
                if (entry.getValue() > maxVotes) {
                    maxVotes = entry.getValue();
                    bestLabel = entry.getKey();
                }
            }
            return bestLabel;
        }

        private static class DistanceRecord {
            Instance instance; double distance;
            DistanceRecord(Instance instance, double distance) {
                this.instance = instance; this.distance = distance;
            }
        }
    }

    // ==========================================
    // 步骤3：交叉验证计算准确率、精度和召回率
    // ==========================================
    static class Metrics {
        double accuracy; double macroPrecision; double macroRecall;
        public Metrics(double accuracy, double macroPrecision, double macroRecall) {
            this.accuracy = accuracy; this.macroPrecision = macroPrecision; this.macroRecall = macroRecall;
        }
    }

    public static Metrics evaluate(List<String> yTrue, List<String> yPred) {
        Set<String> classes = new HashSet<>(yTrue);
        int correct = 0;
        Map<String, Integer> TP = new HashMap<>();
        Map<String, Integer> FP = new HashMap<>();
        Map<String, Integer> FN = new HashMap<>();

        for (String c : classes) { TP.put(c, 0); FP.put(c, 0); FN.put(c, 0); }

        for (int i = 0; i < yTrue.size(); i++) {
            String t = yTrue.get(i); String p = yPred.get(i);
            if (t.equals(p)) { correct++; TP.put(t, TP.get(t) + 1); } 
            else { FP.put(p, FP.getOrDefault(p, 0) + 1); FN.put(t, FN.get(t) + 1); }
        }

        double accuracy = (double) correct / yTrue.size();
        double macroPrecision = 0.0; double macroRecall = 0.0;
        
        for (String c : classes) {
            int tp = TP.get(c); int fp = FP.get(c); int fn = FN.get(c);
            macroPrecision += (tp + fp == 0) ? 0 : (double) tp / (tp + fp);
            macroRecall += (tp + fn == 0) ? 0 : (double) tp / (tp + fn);
        }
        return new Metrics(accuracy, macroPrecision / classes.size(), macroRecall / classes.size());
    }

    public static Metrics kFoldCrossValidation(List<Instance> dataset, int kFold, int knnK) {
        List<Instance> shuffled = new ArrayList<>(dataset);
        Collections.shuffle(shuffled, new Random(42)); 

        int foldSize = shuffled.size() / kFold;
        List<String> allTrue = new ArrayList<>();
        List<String> allPred = new ArrayList<>();

        for (int i = 0; i < kFold; i++) {
            int start = i * foldSize;
            int end = (i == kFold - 1) ? shuffled.size() : (i + 1) * foldSize;

            List<Instance> valSet = new ArrayList<>(shuffled.subList(start, end));
            List<Instance> trainSet = new ArrayList<>();
            trainSet.addAll(shuffled.subList(0, start));
            trainSet.addAll(shuffled.subList(end, shuffled.size()));

            StandardScaler scaler = new StandardScaler();
            scaler.fit(trainSet);
            List<Instance> scaledTrain = scaler.transform(trainSet);
            List<Instance> scaledVal = scaler.transform(valSet);

            KNNClassifier knn = new KNNClassifier(knnK);
            knn.fit(scaledTrain);

            for (Instance valInst : scaledVal) {
                allTrue.add(valInst.label);
                allPred.add(knn.predict(valInst));
            }
        }
        return evaluate(allTrue, allPred);
    }

    public static List<Instance> loadData(String filename) throws IOException {
        List<Instance> data = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                String[] parts = line.split(",");
                double[] features = new double[parts.length - 1];
                for (int i = 0; i < parts.length - 1; i++) features[i] = Double.parseDouble(parts[i]);
                data.add(new Instance(features, parts[parts.length - 1]));
            }
        }
        return data;
    }

    // ==========================================
    // 步骤4：Swing 图形化验证结果可视化 (折线图)
    // ==========================================
    static class ResultChart extends JPanel {
        List<Integer> ks;
        List<Double> accuracies;

        public ResultChart(List<Integer> ks, List<Double> accuracies) {
            this.ks = ks;
            this.accuracies = accuracies;
            setPreferredSize(new Dimension(600, 400));
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            int padding = 60;
            int w = getWidth() - 2 * padding;
            int h = getHeight() - 2 * padding;

            // 画坐标轴背景线
            g2.setColor(Color.LIGHT_GRAY);
            for (int i = 0; i <= 5; i++) {
                int yLine = padding + h - (i * h / 5);
                g2.drawLine(padding, yLine, padding + w, yLine);
            }

            // 画坐标轴
            g2.setColor(Color.BLACK);
            g2.drawLine(padding, padding + h, padding + w, padding + h); // X轴
            g2.drawLine(padding, padding + h, padding, padding);         // Y轴
            
            g2.drawString("K Value", padding + w / 2 - 20, padding + h + 40);
            g2.drawString("Accuracy", 10, padding - 10);

            // 计算Y轴范围
            double minAcc = Collections.min(accuracies);
            double maxAcc = Collections.max(accuracies);
            double yMin = Math.max(0.0, minAcc - 0.02); 
            double yMax = Math.min(1.0, maxAcc + 0.02); 
            if (yMax == yMin) { yMax += 0.1; yMin -= 0.1; }

            // 标注Y轴刻度
            for (int i = 0; i <= 5; i++) {
                int yLine = padding + h - (i * h / 5);
                double tickVal = yMin + (yMax - yMin) * i / 5.0;
                g2.drawString(String.format("%.1f%%", tickVal * 100), 10, yLine + 5);
            }

            // 计算点的坐标
            Point[] points = new Point[ks.size()];
            for (int i = 0; i < ks.size(); i++) {
                int x = padding + (int) ((double) i / (ks.size() - 1) * w);
                int y = padding + h - (int) ((accuracies.get(i) - yMin) / (yMax - yMin) * h);
                points[i] = new Point(x, y);
            }

            // 画折线
            g2.setColor(Color.BLUE);
            g2.setStroke(new BasicStroke(2f));
            for (int i = 0; i < points.length - 1; i++) {
                g2.drawLine(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y);
            }

            // 画数据点和文本
            for (int i = 0; i < points.length; i++) {
                g2.setColor(Color.RED);
                g2.fillOval(points[i].x - 4, points[i].y - 4, 8, 8);
                
                g2.setColor(Color.BLACK);
                g2.drawString(String.valueOf(ks.get(i)), points[i].x - 5, padding + h + 20); // X轴刻度
                
                String accStr = String.format("%.2f%%", accuracies.get(i) * 100);
                g2.drawString(accStr, points[i].x - 15, points[i].y - 10); // 数值
            }
        }
    }

    public static void showGUIChart(List<Integer> ks, List<Double> accuracies) {
        JFrame frame = new JFrame("KNN Validation Results");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new ResultChart(ks, accuracies));
        frame.pack();
        frame.setLocationRelativeTo(null); 
        frame.setVisible(true);
    }

    // ==========================================
    // 主函数
    // ==========================================
    public static void main(String[] args) {
        try {
            String dataFile = "/Users/darren/Desktop/ML/1/iris.data"; 
            
            System.out.println("正在读取文件: " + dataFile);
            List<Instance> dataset = loadData(dataFile);

            int kFold = 5;
            List<Integer> kValues = Arrays.asList(1, 3, 5, 7, 9, 11, 13, 15);
            List<Double> accuracies = new ArrayList<>();

            System.out.printf("\n开始 %d 折交叉验证...\n", kFold);
            System.out.printf("%-5s | %-10s | %-15s | %-15s\n", "K", "Accuracy", "Precision", "Recall");
            System.out.println("---------------------------------------------------------");

            for (int k : kValues) {
                Metrics metrics = kFoldCrossValidation(dataset, kFold, k);
                accuracies.add(metrics.accuracy);
                System.out.printf("%-5d | %.4f     | %.4f          | %.4f\n", 
                        k, metrics.accuracy, metrics.macroPrecision, metrics.macroRecall);
            }

            System.out.println("\n正在生成可视化折线图窗口 (如果没看到，请查看底部 Dock 栏是否有新弹出的 Java 图标)...");
            showGUIChart(kValues, accuracies);
            
        } catch (Exception e) {
            System.err.println("出错: " + e.getMessage());
        }
    }
}