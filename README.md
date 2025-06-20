<h4 class="text-center">Wordle, but it doesn't like you very much.</h4>
<a href="https://fluffyponyy.itch.io/nordle"> Itch.io link </a>
<p class="text-center">Submission for Besties Game Jam 2025, with theme:&nbsp;"Make me feel an emotion." (target emotion: <strong>anger</strong>)</p>
<h3 class="text-center">How to Play</h3>
<p>Enter a guess for the secret word. Correct&nbsp;letters in correct positions&nbsp;appear in hot pink, correct letters in the wrong position appear in yellow, and letters that are not in the secret word appear in grey. You can play again after inputting 6 guesses by pressing "enter". If you fail in 6 guesses, you can also view all or some of the remaining possible words.</p>
<h3 class="text-center">Credits</h3>
<ul><li>Referenced&nbsp;<a target="_blank" href="https://qntm.org/absurdle">Absurdle dev notes</a></li><li>Some UI code generated by an LLM</li><li>Heart pixel art by <a href="https://sabrina-ross.itch.io/" target="_blank">@sabrina_ross</a></li><li>Font is "Gold" from <a href="https://somepx.itch.io/humble-fonts-gold" target="_blank">Humble Fonts</a> asset pack</li><li>Wordle word lists from <a href="https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt" target="_blank">here</a><a href="https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d#file-wordle-la-txt" target="_blank"></a></li></ul>
<h3 class="text-center">Tools</h3>
<ul><li>Programmed in Python with Pygame for UI</li><li>Pygbag to create web build</li></ul>
<h3 class="text-center">Notes</h3>
<p>After having the idea for a Wordle that changes the word with each guess, I found Absurdle online. I decided to implement my own algorithm for an "evil Wordle" that differs from Absurdle in two ways:</p>
<ul><li>Chooses next grouping of words based on lowest number of greens/yellows</li><li>Sometimes nondeterministic (whenever two or more groups of words tie for&nbsp;the lowest number of greens/yellow, one group is selected randomly)</li></ul>
<p>I also chose to keep it limited to 6 tries like classic Wordle, since it is not quite as difficult as Absurdle.</p>
