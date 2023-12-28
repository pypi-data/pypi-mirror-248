import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { DOMUtils } from '@jupyterlab/apputils';
import {Widget} from '@lumino/widgets';

const iBeamer_Anchor_CSS_CLASS = 'jp-iBeamer-Anchor';

/**
 * Initialization data for the iBeamer extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'iBeamer:plugin',
  description: 'A simple .css Beamer/LaTeX Environment Extension for Jupyter Lab/Notebooks',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('iBeamer is activated!');

    const node = document.createElement('div');
    node.innerHTML = "<a href='https://www.lambda.joburg' target='_blank'> <img src='https://lambda.joburg/assets/images/index/logo/lambda_logo.svg' /> </a>";

    const widget = new Widget({node});
    widget.id = DOMUtils.createDomID();
    widget.addClass(iBeamer_Anchor_CSS_CLASS);
    
    app.shell.add(widget, 'top', {rank: 1000});
  }
};

export default plugin;
