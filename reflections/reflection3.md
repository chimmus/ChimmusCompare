# Describe the most recent task were you trying to complete? 
we was tryna figure out how to make the 
candlestick work
# Describe in 2 sentences the task or challenge you were working on. What problem were you trying to solve? 

Your response: 

We decided to experiment with click 

We will implement that later once we understand the code 

 

# How did you use AI if you used it at all? 

Include the prompts you gave to AI (e.g., ChatGPT, GitHub Copilot), what it responded with, and how you used or changed its suggestions. Paste screenshots of the prompts you put into AI or paste a link to your conversation. 

 
Here is my conversation: 
I’m confirming what `plotext` supports for series styling so the change is based on the library’s real behavior, not guesswork. 

 dlestick))\nprint(plt.candlestick.__doc__)\n", 

  "workingDirectory": "c:/Users/lim.m1/repos/comparison/ChimmusCompare", 

  "timeout": 120000 

} 

  

Read [](file:///c%3A/Users/lim.m1/repos/comparison/ChimmusCompare/request.py#45-45), lines 45 to 120 

  

I’ve confirmed the library has a built-in `label` option for series names, so I’m wiring that into the chart and verifying the plotting calls themselves don’t throw. 

  

✅ Updated 

  

I updated request.py so each candlestick series is now tied to a symbol. 

  

Expected result 

When you run the script and enter two symbols, the chart should now let you tell which candlestick belongs to which symbol by: 

- the legend label in the plot, and 

- the color difference between the two series 

  

> I verified the plotting calls themselves, but the terminal rendering in this tool environment hit a Unicode encoding issue on show(), so the final visual display still depends on your terminal setup. 

  

Made changes. 
 
 
Your response: 

 


hat did you learn? 
# Did you use AI help you understand any concepts? Did you accept its suggestions as-is, change them, or decide not to use them. What did you learn in this lesson in general? 

Your response: we learnt how to use the click library and how to make a candle stick 

We also did some writing of documentation 

 

# How did you use Github and git commits to manage your workflow? 

See if you can find your commit history to show the progress of your work so far, paste a screenshot of it below. 

We used it to commit to the project 😊 

https://www.youtube.com/watch?v=Ge-RxCjyHh8 