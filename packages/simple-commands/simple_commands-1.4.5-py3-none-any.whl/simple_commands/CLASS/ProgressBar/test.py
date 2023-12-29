from progressBar import ProgressBar
ProgressBar.set_start()
for i in ProgressBar.generate(range(2)):
    ProgressBar.Progress_print(i ** 2)
