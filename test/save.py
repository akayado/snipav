import sys, os
sys.path.append(os.curdir)
from qtpy import QtWidgets, QtGui
from lunasane.i18n import _
from lunasane.ui.timeline import TimelineUI
from lunasane.data.project import Project, project_from_id, project_from_path
from lunasane.data.track import Track
from lunasane.data.fullids import full_id_from_instance, full_id_from_id, relative_full_id, full_id_to_instance

def main():
    app = QtWidgets.QApplication(sys.argv)

    proj = Project.load('test/test1.json')

    print(proj.to_json(proj.abspath))

if __name__ == "__main__":
    main()
