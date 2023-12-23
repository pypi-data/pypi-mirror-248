Changelog
=========

0.1.3 (2023.12.23)
------------------

* Defaulting to no-plotting on windows to avoid an error caused by tkinter
* Retry scenario generation on failure. This is useful for piece-wise linear which will fail (by design) if n_pareto happened to be less than n_segments + 1

0.1.2 (2023.12.18)
------------------

* Adding better scenario generation and supporting mixtures of zero-sum, monotonic and general scenarios.
* Requiring negmas 0.10.8

0.1.2 (2023.12.11)
------------------

* Controlling log path in anl2024_tournament() through the added base_path argument

0.1.1 (2023.12.09)
------------------
* Added anl cli for running tournaments.
* Added the ability to hide or show type names during negotiations
* Corrected a bug in importing unique_name
* Now requires negmas 0.10.6

0.1.0 (2023.11.30)
------------------

* Adding ANL 2024 placeholder
