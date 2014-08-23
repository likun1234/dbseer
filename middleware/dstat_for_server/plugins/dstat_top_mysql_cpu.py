### Authority: Dag Wieers <dag@wieers.com>

class dstat_plugin(dstat):
    """
    Most expensive CPU process.

    Displays the mysql process that uses the CPU the most during the monitored
    interval. The value displayed is the percentage of CPU time for the total
    amount of CPU processing power. Based on per process CPU information.
    """
    def __init__(self):
        self.name = 'mysql_cpu'
        self.vars = ('mysql_cpu',)
        self.type = 's'
        self.width = 9
        self.scale = 0
        self.pidset1 = {}; self.pidset2 = {}

    def extract(self):
        self.val['max'] = 0
#self.val['mysql-cpu'] = ''
        self.val['mysql_cpu'] = '%s' % (cprint(0.0, 'f', 3, 3))
        for pid in proc_pidlist():
            try:
                ### Using dopen() will cause too many open files
                l = proc_splitline('/proc/%s/stat' % pid)
            except IOError:
                continue

            if len(l) < 15: continue

            ### Reset previous value if it doesn't exist
            if not self.pidset1.has_key(pid):
                self.pidset1[pid] = 0

            self.pidset2[pid] = long(l[13]) + long(l[14])
            usage = (self.pidset2[pid] - self.pidset1[pid]) * 1.0 / elapsed / cpunr
            name = l[1][1:-1]
	    proc_name = getnamebypid(pid, name)

            self.val['name'] = 'mysqld'

            ### Is it a new topper ?
            if usage < self.val['max'] or proc_name != "mysqld": continue


            self.val['max'] = usage
            self.val['pid'] = pid
            self.val['name'] = getnamebypid(pid, name)
#            self.val['name'] = name

#        if self.val['max'] != 0.0:
#self.val['mysql-cpu'] = '%-*s%s' % (self.width-3, self.val['name'][0:self.width-3], cprint(self.val['max'], 'f', 3, 34))
        self.val['mysql_cpu'] = '%s' % (cprint(self.val['max'], 'f', 3, 34))

        ### Debug (show PID)
#        self.val['cpu process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

        if step == op.delay:
            self.pidset1.update(self.pidset2)

    def showcsv(self):
        return '%d' % (self.val['max'])

# vim:ts=4:sw=4:et
