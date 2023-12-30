import { JupyterFrontEnd } from '@jupyterlab/application';
import { CellButton } from './CellButton';
import { NotebookButton } from './NotebookButton';
import { NotebookPanel } from '@jupyterlab/notebook';

// function that adds the multiple notebook buttons associated with the dashboards
export const addDashboardNotebookExtensions = (app: JupyterFrontEnd): void => {
  // since the plugin activation is async, some noteboks might have already been created without the buttons
  for (const w of app.shell.widgets()) {
    if (w instanceof NotebookPanel) {
      const panel = w as NotebookPanel;
      const notebookButton = new NotebookButton(app.commands);
      const cellButton = new CellButton(app.commands);

      const notebookButtonDisposable = notebookButton.createNew(panel);
      const cellButtonDisposable = cellButton.createNew(panel);

      panel.disposed.connect(() => {
        notebookButtonDisposable.dispose();
        cellButtonDisposable.dispose();
      });
    }
  }

  // add notebook cell button to future notebooks
  app.docRegistry.addWidgetExtension('Notebook', new CellButton(app.commands));

  // add notebook toolbar button to future notebooks
  app.docRegistry.addWidgetExtension(
    'Notebook',
    new NotebookButton(app.commands)
  );
};
