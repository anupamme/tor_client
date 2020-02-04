import getpass
import sys
import time

import stem
import stem.connection

from stem.control import Controller

from stem.descriptor import DocumentHandler
from stem.descriptor.remote import DescriptorDownloader

NUM_CIRCUITS_PER_GUARD = 1


def print_paths(circ):
    circuit_path = ''
    for i, entry in enumerate(circ.path):
        fingerprint, nickname = entry
        circuit_path = circuit_path + '[' + fingerprint + ', ' + nickname + ']'
    circuit_path = circuit_path + ';\n'
    return circuit_path

if __name__ == '__main__':
  downloader = DescriptorDownloader()
  consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]

  with open('descriptor_dump.start', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))

  with Controller.from_port() as controller:
    controller.authenticate()

    print("Tor is running version %s" % controller.get_version())

    with open('output.txt', 'w') as f:
        for j in range(3600):
            for i in range(NUM_CIRCUITS_PER_GUARD):
                print(j,i)
                circ = controller.extend_circuit('0')
                time.sleep(5)
                rtn = controller.get_circuit(circ, default='')
                if rtn:
                    circuit_path = ''
                    for i, entry in enumerate(rtn.path):
                        fingerprint, nickname = entry
                        circuit_path = circuit_path + '[' + fingerprint + ', ' + nickname + ']'
                    circuit_path = circuit_path + ';\n'
                    f.write(circuit_path)
                    controller.close_circuit(rtn.id)
            controller.drop_guards()
            time.sleep(1)

  consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]
  
  with open('descriptor_dump.end', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))