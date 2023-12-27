/**
 * Set up keyboard shortcuts & commands for notebook
 */
import { CommandRegistry } from '@lumino/commands';
import { CompletionHandler } from '@jupyterlab/completer';
import { NotebookPanel } from '@jupyterlab/notebook';
export declare const SetupCommands: (commands: CommandRegistry, nbWidget: NotebookPanel, handler: CompletionHandler) => void;
