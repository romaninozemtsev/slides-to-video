const puppeteer = require('puppeteer');
const fs = require('fs');

const questionExample = {
    "number": 65,
    "question": "What happened at the Constitutional Convention?",
    "answer": ["The Constitution was written.", "The Founding Fathers wrote the Constitution."]
};



function renderQuestionHtml(question, showAnswer) {
    let answerHtml = '<ul>';
    for (let i = 0; i < question.answer.length; i++) {
        answerHtml += `<li>${question.answer[i]}</li>`;
    }
    answerHtml += '</ul>';

    return `
    <style>
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
      }
      
      .question {
        margin: 2em;
        padding: 1em;
        background-color: #f2f2f2;
        border-radius: 10px;
      }
      
      .question-number {
        font-size: 1.5em;
        color: #4CAF50;
        margin-bottom: 0.5em;
      }
      
      .question-text {
        font-size: 1.2em;
        margin-bottom: 0.5em;
      }
      
      .question-answer {
        visibility: hidden;
        height: auto;
        opacity: 0;
        transition: visibility 0s, opacity 0.5s linear;
        background-color: #cfe3ff;
        border-radius: 10px;
        padding: 1em;
        margin-top: 1em;
      }
      
      .question-answer.active {
        visibility: visible;
        opacity: 1;
      }
      
      .question-answer ul {
        padding-left: 20px;
      }
      
      .question-answer li {
        margin-bottom: 0.5em;
      }
      
    </style>
    <body>
    <div class="question">
        <div class="question-number">${question.number}</div>
        <div class="question-text">${question.question}</div>
        <div class="question-answer ${showAnswer ? 'active': ''}">${answerHtml}</div>
    </div>
    </body>`
}


(async () => {
  let rawQuestions = fs.readFileSync('questions.json');
  let questions = JSON.parse(rawQuestions);
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  for (let i = 0; i < questions.length; i++) {
        let section = questions[i];
        for (let j = 0; j < section.questions.length; j++) {
            let question = section.questions[j];

            await page.setContent(renderQuestionHtml(question, false));
            await page.screenshot({path: `screenshots/${question.number}_q.png`});

            await page.setContent(renderQuestionHtml(question, true));
            await page.screenshot({path: `screenshots/${question.number}_a.png`});
    
        }
    }
  //await page.setContent(renderQuestionHtml());
  //await page.screenshot({path: 'example.png'});

  await browser.close();
})();



