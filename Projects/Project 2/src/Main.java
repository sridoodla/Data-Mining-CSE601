import dbscan.DBScan;
import hierarchical.HierarchicalClustering;
import kmeans.KMeans;

import java.io.IOException;

@SuppressWarnings("Duplicates")
public class Main {

    public static void main(String[] args) throws IOException {

        //Variables
        String FILENAME = "new_data_1";

        //DBSCAN
        double EPS = 1;
        int MINPTS = 2;

        //KMEANS
        int NUMCLUSTERS = 5;

        //HIERARCHICAL
        int noOfClusters=5;

        System.out.println("--------------K-Means--------------");
        KMeans kMeans = new KMeans();
        kMeans.main(NUMCLUSTERS,FILENAME);

        System.out.println();
        System.out.println("--------------DBSCAN--------------");
        System.out.println();
        DBScan dbScan = new DBScan();
        dbScan.main(EPS, MINPTS, FILENAME);

        System.out.println();
        System.out.println("--------------Hierarchical--------------");
        HierarchicalClustering hc = new  HierarchicalClustering();
        hc.mainHAC(noOfClusters,FILENAME);


    }


}
