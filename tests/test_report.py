import sys

sys.path.append("../")

from sop.reporter.report import report

ymlfile:"data/report.yml"}

def test_report():
    report(ymlfile)


if __name__ == "__main__":
    test_report()


