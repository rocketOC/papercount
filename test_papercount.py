import unittest
import papercount

class TestPaper(unittest.TestCase):

	def test_network_counting_black_background_4(self):
		papercount.loadnew(filename='TestImages/test_count_4_b.png',bg_value=0)
		nets = papercount.network_search()
		self.assertEqual(len(nets),4)

	def test_network_counting_white_background_4(self):
		papercount.loadnew(filename='TestImages/test_count_4_w.png',bg_value=255)
		nets = papercount.network_search()
		self.assertEqual(len(nets),4)

	def test_network_counting_black_background_12(self):
		papercount.loadnew(filename='TestImages/test_count_12_b.png',bg_value=0)
		nets = papercount.network_search()
		self.assertEqual(len(nets),12)

	def test_network_counting_white_background_12(self):
		papercount.loadnew(filename='TestImages/test_count_12_w.png',bg_value=255)
		nets = papercount.network_search()
		self.assertEqual(len(nets),12)

	def test_get_next_none(self):
		papercount.loadnew(filename='TestImages/test_next_w1.png',bg_value=0)
		next = papercount.get_next(1,1,3,3)
		self.assertEqual(len(next),0)

	def test_get_next_8(self):
		papercount.loadnew(filename='TestImages/test_next_w9.png',bg_value=0)
		next = set(papercount.get_next(1,1,3,3))
		self.assertEqual(len(next),8)

	def test_get_next_4(self):
		papercount.loadnew(filename='TestImages/test_next_b5.png',bg_value=0)
		next = set(papercount.get_next(1,1,3,3))
		self.assertEqual(len(next),4)

	def test_count_blacks_in_image(self):
		papercount.loadnew(filename='TestImages/test_next_b5.png',bg_value=0)
		black_count = papercount.count_blacks_in_image()
		self.assertEqual(black_count,5)

	def test_bin_value_none(self):
		bins = (0,5,10,15,20)
		mybin = papercount.bin_value(value=25,bins=bins)
		self.assertIsNone(mybin)

	def test_bin_value_lastbin(self):
		bins = (0,5,10,15,20)
		mybin = papercount.bin_value(value=20,bins=bins)
		self.assertEqual(mybin,17.5)

	def test_bin_value_leftclosure(self):
		bins = (0,5,10,15,20)
		mybin = papercount.bin_value(value=15,bins=bins)
		self.assertEqual(mybin,17.5)

if __name__ == '__main__':
	unittest.main()