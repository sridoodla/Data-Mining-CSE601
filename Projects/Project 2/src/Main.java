import dbscan.DBScan;
import kmeans.KMeans;

import java.io.FileNotFoundException;

@SuppressWarnings("Duplicates")
public class Main {

    public static void main(String[] args) throws FileNotFoundException {

        //Variables

        //DBSCAN
        double EPS = 1;
        int MINPTS = 2;
        String FILENAME = "new_data_1";

        //KMEANS


        //HIERARCHICAL

        System.out.println("--------------K-Means--------------");
        KMeans kMeans = new KMeans();
        kMeans.main();

        System.out.println("--------------DBSCAN--------------");
        System.out.println();
        DBScan dbScan = new DBScan();
        dbScan.main(EPS, MINPTS, FILENAME);

        System.out.println("--------------Hierarchical--------------");


    }


}
