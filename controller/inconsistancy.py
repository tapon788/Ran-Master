__author__ = 'tpaul'

class Inconsistancy:
    def __init__(self):
        self.get_primary_info_db()
        self.processing()
        self.get_seconday_info_db()
        pass

    def get_primary_info_db(self):
        db = MySQLdb.connect('localhost', 'root', '', 'myrncml')
        cursor = db.cursor()
        query ="select bsc,bcf,bts,adjcindex,adjcellbsicbcc,adjcellbsicncc,bcchfrequency," \
               "count(concat(adjcellbsicbcc,adjcellbsicncc,bcchfrequency)) \`tot\` from adce group by bsc,bcf,bts,concat(adjcellbsicbcc,adjcellbsicncc,bcchfrequency) having \`tot\`>1;"
        print "Primary"




    def get_seconday_info_db(self):
        print "Secondary"
    def processing(self):
        print "Processing"

if __name__ == '__main__':
    aInconsistancy = Inconsistancy()
