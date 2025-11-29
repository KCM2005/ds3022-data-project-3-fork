import requests
import os
import sys
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='analysis.log')
logger=logging.getLogger(__name__)

def analyze_commits():
    # con=duckdb.connect(database='packages.duckdb',read_only=False)
    con=duckdb.connect(database='packages.duckdb',read_only=True)

    logger.info("Connected to DuckDB database for analysis.")

    try:
        commit_count=con.execute("""SELECT DISTINCT package as package, COUNT(*) as package_count FROM commits GROUP BY package;""").fetchall()
        commit_counts_df=pd.DataFrame(commit_count, columns=['package', 'package_count'])
        logger.info("Fetched commit counts per package.")

        plt.figure(figsize=(10,6))
        plt.bar(commit_counts_df['package'], commit_counts_df['package_count'], color='skyblue')
        plt.xlabel('Package')
        plt.ylabel('Number of Commits')
        plt.title('Number of Commits per Package')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('commit_counts_per_package.png')
        logger.info("Saved commit counts bar chart as commit_counts_per_package.png.")
        print( commit_counts_df)
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")

    
def visualize_hourly_commits():
    con=duckdb.connect(database='packages.duckdb',read_only=True)
    logger.info("Connected to DuckDB database for visualizing hourly commits via graph.")

    try:
        commit_counts_hourly=con.execute("""SELECT
                                            package,
                                            EXTRACT(hour FROM date) AS hour,
                                            COUNT(*) AS commits
                                        FROM commits
                                        GROUP BY package, hour
                                        ORDER BY package, hour;""").df()
        logger.info("Fetched commit counts per package, hourly.")

        plt.clf()

        # pandas hourly
        pandas_df = commit_counts_hourly[commit_counts_hourly['package'] == 'pandas']
        plt.plot(pandas_df['hour'], pandas_df['commits'], color='#274c77', label='pandas')
        logger.info("finished plotting pandas hours in the day")

        # matplotlib hourly
        matplolib_df = commit_counts_hourly[commit_counts_hourly['package'] == 'matplotlib' ]
        plt.plot(matplolib_df['hour'], matplolib_df['commits'], color='#d62828', label='matplotlib')
        logger.info("finished plotting matplotlib hours in the day")

        # plotly hourly
        plotly_df = commit_counts_hourly[commit_counts_hourly['package'] == 'plotly' ]
        plt.plot(plotly_df['hour'], plotly_df['commits'], color='#f77f00', label='plotly')
        logger.info("finished plotting plotly hours in the day")

        # numpy hourly
        numpy_df = commit_counts_hourly[commit_counts_hourly['package'] == 'numpy' ]
        plt.plot(numpy_df['hour'], numpy_df['commits'], color='#fcbf49', label='numpy')
        logger.info("finished plotting numpy hours in the day")

        hours = list(range(25))
        labels = [
            "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM",
            "8 AM", "9 AM", "10 AM", "11 AM",
            "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM",
            "8 PM", "9 PM", "10 PM", "11 PM", "12 AM"
        ]
        every_other = hours[::3]
        every_other_labels = labels[::3]
        plt.xticks(every_other, every_other_labels)
                
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.title("Commits per Hour for pandas, matplotlib, plotly, and numpy", y=1.05, x=0.43)
        # plt.text(5.75, 3130, "pandas,", size=12, color='#274c77')
        # plt.text(9.5, 3130, "matplotlib,", size=12, color='#d62828')
        # plt.text(14.5, 3130, "plotly,", size=12, color='#f77f00')
        # plt.text(17.5, 3130, "and ", size=12, color='black')
        # plt.text(19.5, 3130, "numpy", size=12, color='#fcbf49')

        # plt.text(-3.8, 2750, "(commits)", size=10)
        plt.legend()
        plt.ylabel("commits")
        plt.xlabel("hours in the day")

        plt.savefig("hourly_commits.png")

        logger.info("finished plotting commits per hour in the day (24)")

    except Exception as e:
        logging.error(f"An error occurred during hourly visualizations: {e}")


def visualize_daily_commits():
    con=duckdb.connect(database='packages.duckdb',read_only=True)
    logger.info("Connected to DuckDB database for visualizing daily commits via graph.")

    try:
        commit_counts_daily=con.execute("""SELECT
                                                package,
                                                EXTRACT(doy FROM date) AS day_of_year,
                                                COUNT(*) AS commits
                                            FROM commits
                                            GROUP BY package, day_of_year
                                            ORDER BY package, day_of_year;""").df()
        logger.info("Fetched commit counts per package, daily.")

        plt.clf()

        # pandas daily
        pandas_df = commit_counts_daily[commit_counts_daily['package'] == 'pandas']
        plt.plot(pandas_df['day_of_year'], pandas_df['commits'], color='#274c77', label='pandas')
        logger.info("finished plotting pandas day of year")

        # matplotlib daily
        matplolib_df = commit_counts_daily[commit_counts_daily['package'] == 'matplotlib' ]
        plt.plot(matplolib_df['day_of_year'], matplolib_df['commits'], color='#d62828', label='matplotlib')
        logger.info("finished plotting matplotlib day of year")

        # plotly daily
        plotly_df = commit_counts_daily[commit_counts_daily['package'] == 'plotly' ]
        plt.plot(plotly_df['day_of_year'], plotly_df['commits'], color='#f77f00', label='plotly')
        logger.info("finished plotting plotly day of year")

        # numpy daily
        numpy_df = commit_counts_daily[commit_counts_daily['package'] == 'numpy' ]
        plt.plot(numpy_df['day_of_year'], numpy_df['commits'], color='#fcbf49', label='numpy')
        logger.info("finished plotting numpy day of year")
                
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.title("Commits per Day for pandas, matplotlib, plotly, and numpy", y=1.05, x=0.43)
        # plt.text(5.75, 1, "pandas,", size=12, color='#274c77')
        # plt.text(9.5, 1, "matplotlib,", size=12, color='#d62828')
        # plt.text(14.5, 1, "plotly,", size=12, color='#f77f00')
        # plt.text(17.5, 1, "and ", size=12, color='black')
        # plt.text(19.5, 1, "numpy", size=12, color='#fcbf49')

        # plt.text(-3.8, 100, "(commits)", size=10)
        plt.legend()
        plt.ylabel("commits")
        plt.xlabel("days in the year")

        plt.savefig("daily_commits.png")

        logger.info("finished plotting commits per day of year (365)")

    except Exception as e:
        logging.error(f"An error occurred during daily visualizations: {e}")


def visualize_weekly_commits():
    con=duckdb.connect(database='packages.duckdb',read_only=True)
    logger.info("Connected to DuckDB database for visualizing weekly commits via graph.")

    try:
        commit_counts_weekly=con.execute("""SELECT
                                                package,
                                                DATE_TRUNC('week', date) AS week,
                                                COUNT(*) AS commits
                                            FROM commits
                                            GROUP BY package, week
                                            ORDER BY package, week;""").df()
        logger.info("Fetched commit counts per package, weekly.")

        plt.clf()

        # pandas weekly
        pandas_df = commit_counts_weekly[commit_counts_weekly['package'] == 'pandas']
        plt.plot(pandas_df['week'], pandas_df['commits'], color='#274c77', label='pandas')
        logger.info("finished plotting pandas weekly")

        # matplotlib weekly
        matplolib_df = commit_counts_weekly[commit_counts_weekly['package'] == 'matplotlib' ]
        plt.plot(matplolib_df['week'], matplolib_df['commits'], color='#d62828', label='matplotlib')
        logger.info("finished plotting matplotlib weekly")

        # plotly weekly
        plotly_df = commit_counts_weekly[commit_counts_weekly['package'] == 'plotly' ]
        plt.plot(plotly_df['week'], plotly_df['commits'], color='#f77f00', label='plotly')
        logger.info("finished plotting plotly weekly")

        # numpy weekly
        numpy_df = commit_counts_weekly[commit_counts_weekly['package'] == 'numpy' ]
        plt.plot(numpy_df['week'], numpy_df['commits'], color='#fcbf49', label='numpy')
        logger.info("finished plotting numpy weekly")
                
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.title("Commits per Week for pandas, matplotlib, plotly, and numpy", y=1.05, x=0.43)
        # plt.text(5.75, 1, "pandas,", size=12, color='#274c77')
        # plt.text(9.5, 1, "matplotlib,", size=12, color='#d62828')
        # plt.text(14.5, 1, "plotly,", size=12, color='#f77f00')
        # plt.text(17.5, 1, "and ", size=12, color='black')
        # plt.text(19.5, 1, "numpy", size=12, color='#fcbf49')

        # plt.text(-3.8, 100, "(commits)", size=10)
        plt.legend()
        plt.ylabel("commits")
        plt.xlabel("weeks in the year")

        plt.savefig("weekly_commits.png")

        logger.info("finished plotting commits per week")

    except Exception as e:
        logging.error(f"An error occurred during weekly visualizations: {e}")


def visualize_monthly_commits():
    con=duckdb.connect(database='packages.duckdb',read_only=True)
    logger.info("Connected to DuckDB database for visualizing monthly commits via graph.")

    try:
        commit_counts_monthly=con.execute("""SELECT
                                                package,
                                                DATE_TRUNC('month', date) AS month,
                                                COUNT(*) AS commits
                                            FROM commits
                                            GROUP BY package, month
                                            ORDER BY package, month;""").df()
        logger.info("Fetched commit counts per package, monthly.")

        plt.clf()

        # pandas monthly
        pandas_df = commit_counts_monthly[commit_counts_monthly['package'] == 'pandas']
        plt.plot(pandas_df['month'], pandas_df['commits'], color='#274c77', label='pandas')
        logger.info("finished plotting pandas monthly")

        # matplotlib monthly
        matplolib_df = commit_counts_monthly[commit_counts_monthly['package'] == 'matplotlib' ]
        plt.plot(matplolib_df['month'], matplolib_df['commits'], color='#d62828', label='matplotlib')
        logger.info("finished plotting matplotlib monthly")

        # plotly monthly
        plotly_df = commit_counts_monthly[commit_counts_monthly['package'] == 'plotly' ]
        plt.plot(plotly_df['month'], plotly_df['commits'], color='#f77f00', label='plotly')
        logger.info("finished plotting plotly monthly")

        # numpy monthly
        numpy_df = commit_counts_monthly[commit_counts_monthly['package'] == 'numpy' ]
        plt.plot(numpy_df['month'], numpy_df['commits'], color='#fcbf49', label='numpy')
        logger.info("finished plotting numpy monthly")
                
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        plt.title("Commits per Month for pandas, matplotlib, plotly, and numpy", y=1.05, x=0.43)
        # plt.text(5.75, 1, "pandas,", size=12, color='#274c77')
        # plt.text(9.5, 1, "matplotlib,", size=12, color='#d62828')
        # plt.text(14.5, 1, "plotly,", size=12, color='#f77f00')
        # plt.text(17.5, 1, "and ", size=12, color='black')
        # plt.text(19.5, 1, "numpy", size=12, color='#fcbf49')

        # plt.text(-3.8, 100, "(commits)", size=10)
        plt.legend()
        plt.ylabel("commits")
        plt.xlabel("months in the year")

        plt.savefig("monthly_commits.png")

        logger.info("finished plotting commits per month")

    except Exception as e:
        logging.error(f"An error occurred during monthly visualizations: {e}")



# def format_obtain ():
#     con = duckdb.connect(database='packages.duckdb',read_only=True)
#     print(con.execute("DESCRIBE commits").df())


if __name__ == "__main__":
    analyze_commits()
    # format_obtain()
    visualize_hourly_commits()
    visualize_daily_commits()
    visualize_weekly_commits()
    visualize_monthly_commits()