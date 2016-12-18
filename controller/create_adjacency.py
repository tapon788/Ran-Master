__author__ = 'tpaul'

import MySQLdb
from tkMessageBox import showinfo,showwarning
import time
import _mysql_exceptions
class CreateAdjacency:
    def __init__(self, in_input_dir, in_input_count, in_update_flag, in_db_del_flag, in_adjtype):
        self.input_dir = in_input_dir
        self.input_count = in_input_count
        self.update_flag = in_update_flag
        self.db_del_flag = in_db_del_flag
        self.adjType = in_adjtype
        self.mccKey, self.mncKey, self.lacKey, self.ciKey = "", "", "", ""
        self.setup_variables()
        pass

    def update_adjgtable(self, plmn, adjgid, in_tlac, in_tcid):
        db = MySQLdb.connect('localhost', 'root', '', 'myrncml')
        cursor = db.cursor()
        update_query = "insert into "+self.adjType+" (plmn,"+self.adjType+","+self.adjType+"LAC,"\
                       + self.adjType+"CI" + ") values(\""+plmn+"\","+str(adjgid)+','\
                       + str(in_tlac)+","+str(in_tcid)+");"

        print update_query
        cursor.execute(update_query);
        cursor.close()
        db.commit()
        pass

    def delete_from_db(self):
        db = MySQLdb.connect('localhost','root','','myrncml')
        cursor = db.cursor()
        cursor.execute("Delete from "+self.adjType+" where rnc is null and wbts is null and wcel is null;")
        cursor.close()
        db.commit()
        pass

    def get_adj_from_sql(self, xl_input, progress, var_label_count, error_button_flag):
        fp_troubleshoot = open('C:\Python27\Adjacency\\troubleshoot.txt', 'a')

        progress['value'] = 0
        print xl_input.keys()
        progress['maximum'] = len(xl_input['sourceLac'])
        dist_name_array = []
        count = 0
        print self.input_dir
        error_file = open(self.input_dir + "/warning.log", 'w+')
        error_button_flag.set('0')

        for slac, scid, tlac, tcid in zip(xl_input.get('sourceLac'), xl_input.get('sourceCI'),
                                          xl_input.get(self.lacKey), xl_input.get(self.ciKey)):
            count += 1
            adj_index_array = []
            slac = str(slac)
            scid = str(scid)
            tlac = str(tlac)
            tcid = str(tcid)

            var_label_count.set(str(count)+"/")
            if count <= len(xl_input['sourceLac']):
                progress['value'] = count
                progress.update()

            db = MySQLdb.connect('localhost', 'root', '', 'myrncml')
            cursor = db.cursor()
            query_sub_string = " lac ="+slac+" and CID="+scid+";"
            dump = range(1, 32)
            cmd = "select plmn from wcel where "+query_sub_string
            fp_troubleshoot.write("SQL:"+time.ctime()+":"+cmd+'\n')
            try:
                cursor.execute(cmd)
            except _mysql_exceptions.ProgrammingError, err:
                print err.args[1]
                fp_troubleshoot.close()
                return {'error': err.args[1]}

            data = cursor.fetchall()
            try:
                plmn = data[0][0]
            except IndexError:
                plmn = 'PLMN-PLMN/RNC-0/WBTS-0/WCEL-0'
                error_file.write("Missing: Source cell "+slac+scid+" not found in NOKIA database \n")
                dist_name_array.append(plmn+"/"+self.adjType+"-0")
                error_button_flag.set('1')
                continue

            query_sub_string = " and "+self.lacKey+"="+str(tlac)+" and " + self.ciKey + "=" + str(tcid)+";"   # change
            cmd = "select "+self.adjType+" from "+self.adjType+" where plmn like \"%"+plmn+"%\""+query_sub_string+";"
            fp_troubleshoot.write("SQL:"+time.ctime()+":"+cmd+'\n')
            cursor.execute(cmd)
            data = cursor.fetchall()

            if self.update_flag == 'U' or self.update_flag == 'E':

                try:
                    dist_name_array.append(plmn+"/"+self.adjType+"-"+str(data[0][0]))
                except:
                    error_button_flag.set('1')
                    dist_name_array.append(plmn+"/"+self.adjType+"-0")
                    error_file.write("Fail: No such relation between Source: "+slac+scid+" to target:" + tlac + tcid + "\n")
            else:

                if len(data) != 0:
                    error_button_flag.set('1')
                    error_file.write("Exist: Already exist Source: "+slac+scid+" to target:" + tlac + tcid + "\n")
                    dist_name_array.append(plmn+"/"+self.adjType+"-0")
                    continue

                cmd = "select "+self.adjType+" from "+self.adjType+" where plmn like \"%"+plmn+"%\";"
                cursor.execute(cmd)
                fp_troubleshoot.write("SQL:"+time.ctime()+":"+cmd+'\n\n')

                data = cursor.fetchall()
                cursor.close()

                for row in data:
                    adj_index_array.append(int(row[0]))

                adj_index_array.sort()
                diff = list(set(dump)-set(adj_index_array))
                try:
                    new_adjg_id = diff[0]

                except IndexError:
                    error_button_flag.set('1')
                    error_file.write("Skip: MAX relation exceeded for Source:"+slac+scid+' and target:'+tlac+tcid+"\n")
                    dist_name_array.append(plmn+"/"+self.adjType+"-0")
                    continue
                dist_name_array.append(plmn+"/"+self.adjType+"-"+str(new_adjg_id))
                self.update_adjgtable(plmn, str(new_adjg_id), str(tlac), str(tcid))

        xl_input['distName'] = dist_name_array
        cursor.close()
        error_file.close()
        if self.lacKey+'NEW' in xl_input.keys():
            del xl_input[self.lacKey]
            xl_input[self.lacKey] = xl_input.pop(self.lacKey+'NEW')
        fp_troubleshoot.close()
        return xl_input

    def delete_adj_sql(self):

        if not self.db_del_flag:
            self.delete_from_db()
            showinfo('Info', "New "+self.adjType+" adjacents not updated to sql db")
        else:
            showinfo('Info', 'New '+self.adjType+' adjacents updated to sql db')
            pass

    def setup_variables(self):

        self.mccKey = self.adjType[0].upper()+self.adjType[1:].lower()+'MCC'
        self.mncKey = self.adjType[0].upper()+self.adjType[1:].lower()+'MNC'
        self.lacKey = self.adjType[0].upper()+self.adjType[1:].lower()+'LAC'
        self.ciKey = self.adjType[0].upper()+self.adjType[1:].lower()+'CI'
        pass

    def get_source_adj(self, in_xl_input, in_adjtype):
        query1 = ""
        for adjlac,adjci in zip(in_xl_input[self.lacKey],in_xl_input[self.ciKey]):
            query1 += self.lacKey+"="+adjlac+" and "+self.ciKey+"="+adjci+" or "

        query = "select T1.lac, T1.cid, T2."+self.lacKey+", T2."+self.ciKey+" from wcel T1 inner join "+in_adjtype+" T2 on " \
            "T1.rnc=T2.rnc and T1.wbts=T2.wbts and T1.wcel=T2.wcel where "+query1[:-4]+";"
        db = MySQLdb.connect('localhost', 'root', '', 'myrncml')
        dictCursor = db.cursor()
        dictCursor.execute(query)
        data = dictCursor.fetchall()

        return dict(zip(('sourceLac', 'sourceCI', self.lacKey, self.ciKey), zip(*data)))

