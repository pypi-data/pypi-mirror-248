import pymqi
from adapya.base.dump import dump

queue_manager = 'CSQ3'
channel = 'CHANNEL.GER' # 'CHANNEL.MM'
host = 'da3f' # 10.20.74.81' # 'DAEY'
port = '1414'
queue_name = 'MM.OUT.Q1'  #   'GER.LOCAL.QUEUE1'
conn_info = '%s:%s' % (host, port)

qmgr = pymqi.connect(queue_manager, channel, conn_info) # 'mm', 'pw')
print('Connected to queue manager %r, channel %r via %r' %
       (queue_manager, channel, conn_info))

queue = pymqi.Queue(qmgr, queue_name)
print('accessing queue %r' % queue_name)

message = queue.get()

dump(message,'Message1 read from MQ')

queue.close()
print('closed queue')

qmgr.disconnect()
print('disconnected from queue manager')
