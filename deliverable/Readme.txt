README:

1. The names and andrew IDs of all group members
	
	Cheng Wang(chengw1), Shenggu Lu(shenggul)

2. How to run your code.

	1. Dataset preparation:

	   * You can choose to use our processed dataset in pickle format:
	        Download pickle-formatted data files from google drive, and extract it to the same directory as main.py
            https://drive.google.com/file/d/0BweYiPG4aspAd0lMOElBdW9md2M/view?usp=sharing

       * To run all the code from source dataset, you have to download all the dataset and load them into mysql as
         instructed in the final report. And change the mysql server address in main.py line 114


    2. install the following dependencies

        pip install sklearn, lda, MySQL-python, nltk

    3. `python main.py` to run the code

        It takes about ~30 min to run all the process on my mac book pro. To save the time, you can comment the `load()`
        function call on line 213 to skip all the feature extraction code and load the feature matrix/ label from pickle
        file instead.
	
3. The nbviewer link that you submitted to the google form
	
	http://nbviewer.jupyter.org/github/lumig242/DuplicationDetectionStackOverflow/blob/master/deliverable/finalReport.ipynb
		
4. Links to any large files that were not submitted directly to Autolab (e.g. data files)

	All pickle formatted data files: https://drive.google.com/file/d/0BweYiPG4aspAd0lMOElBdW9md2M/view?usp=sharing

5. Potential sources: If large parts of your code were taken from or copied from elsewhere (which is OK but needs to be
    cited or referenced), include a list of what parts were taken from where.

	None. For idea references, please refer to the reference section in the report.