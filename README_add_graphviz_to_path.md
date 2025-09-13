## How to Add Graphviz to PATH on Windows

1. **Download and Install Graphviz:**
   - Download the Windows installer from:  
     https://graphviz.gitlab.io/_pages/Download/Download_windows.html
   - Run the installer and complete the installation (default location is usually `C:\Program Files\Graphviz`).

2. **Add Graphviz to your PATH:**
   - Open the Start menu and search for `Environment Variables`.
   - Click on **Edit the system environment variables**.
   - In the System Properties window, click the **Environment Variables** button.
   - In the **System variables** section, scroll and select the `Path` variable, then click **Edit**.
   - Click **New** and add the following path (adjust if you installed to a different location):
     ```
     C:\Program Files\Graphviz\bin
     ```
   - Click **OK** to close all dialogs.

3. **Restart your terminal or IDE** (close and reopen PowerShell, CMD, or your code editor).

4. **Verify the installation:**
   - Open a new terminal and run:
     ```
     dot -V
     ```
   - You should see the Graphviz version information.

Now you can use `plot_model` and other Graphviz-based tools from Python.
