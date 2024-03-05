# thesis_repo
Repo containing scripts and Jupyter notebooks to reproduce the experiments in my PhD thesis, empirical chapter per empirical chapter. 

Contents: 

<ul>
	<li> <b>Chapter 3 </b>: Dataset creation from Common Crawl 
	<li> <b>Chapter 5</b>: Website scraping and Tomotopy modeling 
	<li> <b>Chapter 6</b>: Website Weakly Supervised Classification
		<ul>
		<li>This directory contains the <code>seedword.json</code> file, which is a seed words list for each classification label
		<li>To implement contextualised weak supervision, we used the code in <a href="https://github.com/dheeraj7596/ConWea">ConWea</a>. A guide for implementation can be found in the repo.  
		</ul>
	<li> <b>Chapter 7</b>: Inhomogeneous Ripley's K-function 
		<ul>
		<li>The directory contains 4 files: 
		<ul>
			<li> A <code>requirements.txt</code> file
			<li> <code>simulate_controls.py</code> runs a thinning algorithm to simulate companies with the same distribution as tangible and intangible ones
			<li><code>kinhom_estimation_tutorial.ipynb</code> provides a step by step tutorial of our Python implementation of Ripleys Inhomogeneous K-function based on <a href = "https://github.com/pysal/pointpats">pointpats</a>
			<li><code>kinhom_calcs.py</code> calculates max and min of the Kinhom function on our simulated companies data
		</ul>	
		</ul>
  </ul>
