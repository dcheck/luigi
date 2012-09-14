import luigi, luigi.hadoop, luigi.hdfs
import datetime

# To make this run, you probably want to edit /etc/luigi/client.cfg and add something like:
#
# [hadoop]
# jar: /usr/lib/hadoop-xyz/hadoop-streaming-xyz-123.jar

class InputText(luigi.ExternalTask):
    date = luigi.DateParameter()
    def output(self):
        return luigi.hdfs.HdfsTarget(self.date.strftime('/tmp/text/%Y-%m-%d.txt'))

@luigi.expose
class WordCount(luigi.hadoop.JobTask):
    date_interval = luigi.DateIntervalParameter()

    def requires(self):
        return [InputText(date) for date in self.date_interval.dates()]

    def output(self):
        return luigi.hdfs.HdfsTarget('/tmp/text-count/%s-%d' % (self.date.strftime('%Y-%m-%d'), self.lookback))

    def mapper(self, line):
        for word in line.strip().split():
            yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    luigi.run()
