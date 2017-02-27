import os
import logging
import tempfile
import subprocess
import shutil
import re

 
'''intersect 2 kmer databases to find common kmers'''
class KmcIntersect:
	def __init__(self,first_database, second_database, output_directory, threads,result_database):
		self.logger = logging.getLogger(__name__)
		self.first_database = first_database
		self.second_database = second_database
		self.threads = threads
		self.result_database = result_database
		self.temp_working_dir = tempfile.mkdtemp(dir=output_directory)
		self.kmc_output = ''
		self.common_kmer_count =0

	def kmc_intersect_command(self):
		return ' '.join(['kmc_tools', '-t'+str(self.threads), 'intersect', self.first_database, self.second_database, self.result_database ])
		
	def kmc_histogram_command(self):
		return ' '.join(['kmc_tools', 'histogram', self.result_database, self.output_histogram_file() ])
	
	def output_histogram_file(self):
		return os.path.join(self.temp_working_dir, 'histogram') 
	
	def run(self):
		self.logger.info("Finding kmers")
		subprocess.call(self.kmc_intersect_command(),shell=True)
		subprocess.call(self.kmc_histogram_command(),shell=True)
		self.common_kmer_count = self.num_common_kmers()
	
	def num_common_kmers(self):
		total = 0
		if not os.path.exists(self.output_histogram_file()):
			return 1

		with open(self.output_histogram_file(), 'r') as histogram_file:
			for line in histogram_file:
				kmer_freq = re.split(r'\t+', line)
				total = total + int(kmer_freq[1])
		
		return total
	
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)