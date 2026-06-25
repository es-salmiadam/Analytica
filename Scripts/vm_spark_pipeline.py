from pyspark import SparkContext
import os

# CONFIGURATION
# Now we use the HDFS path!
INPUT_FILE = "/user/cloudera/dataset.csv"
# We still save the final SMALL result to the Shared Folder for Windows
OUTPUT_FILE = "/media/sf_PFE101/data/Processed/daily_stats_spark.csv"

def main():
    sc = SparkContext(appName="PFE_Professional_HDFS")
    print("--- STARTING PROFESSIONAL HDFS ANALYSIS ---")

    # 1. Load Data from HDFS
    print("Reading file from HDFS: " + INPUT_FILE)
    lines = sc.textFile(INPUT_FILE)
    
    # 2. Parser
    def parse_line(line):
        try:
            parts = line.split(",")
            # Date is in the 2nd column
            date_str = parts[1].strip()
            if "-" in date_str:
                day = date_str.split(" ")[0]
                if len(day) == 10:
                    return day
            return None
        except:
            return None

    # 3. Aggregation
    print("Processing Big Data in Spark...")
    daily_counts = lines.map(parse_line) \
                       .filter(lambda x: x is not None) \
                       .map(lambda day: (day, 1)) \
                       .reduceByKey(lambda a, b: a + b) \
                       .collect()

    # 4. Save result
    if len(daily_counts) > 0:
        print("SUCCESS! Found " + str(len(daily_counts)) + " days of data.")
        try:
            with open(OUTPUT_FILE, "w") as f:
                f.write("day,nb_tweets\n")
                for day, count in sorted(daily_counts):
                    f.write(str(day) + "," + str(count) + "\n")
            print("Final CSV saved to Shared Folder: " + OUTPUT_FILE)
        except Exception as e:
            print("Error writing CSV: " + str(e))
    else:
        print("ERROR: No data found in HDFS file.")

if __name__ == "__main__":
    main()
