const token = document.querySelector('#csrf input').value;

new Vue({
  el: "main",
  delimiters: ['${', '}'],
  data: {
    questions: [],
    currentQuestion: null,
    numQuestions: null,
    popTexts: [
      'You are about to begin the examination. Click on the Start Test button to continue.',
      'Are you sure you want to submit?',
      'Oops! You are out of time, please exit the hall.',
      'You have successfully completed the examination, you can now exit the hall.'
    ],
    popText: 'Loading questions...',
    showPop: true,
    duration: null,
    answered: null,
    confirmSub: null,
    ongoing: null,
    answerSheet: null,
    notStarted: null,
    sid: +document.getElementById("std").value,
    eid: +document.getElementById("eid").value
  },
  methods: {
    start () {
      this.ongoing = true
      this.showPop = false
      this.notStarted = false
    },
    gotoButton (i) {
      return {
        'goto-tile': true,
        current: i === this.currentQuestion,
        selected: !!this.answerSheet.answers[i].selected_option
      }
    },
    chooseAnswer (option) {
      const question = this.answerSheet.answers[this.currentQuestion]
      if (!question.selected_option) this.answered++
      question.selected_option = option
    },
    move (n) {
      this.currentQuestion = (n + this.currentQuestion) % this.numQuestions
    },
    submit () {
      this.ongoing = false
      this.confirmSub = false
      this.popText = "Submitting your answers..."
      fetch('/api/examination/submit', {
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': token,
          'X-Requested-With': 'XMLHttpRequest'
        },
        method: 'POST',
        body: JSON.stringify(this.answerSheet)
      })
        .then(res => res.json())
        .then(resp => {
          if (resp.success) {
            this.popText = "Submitted! You can exit the hall now."
          } else {
            this.popText = "An error occurred"
            console.log(resp)
          }
        })
        .catch(e => this.popText = e)
    },
    confirmSubmit () {
      this.popText = this.popTexts[1]
      this.confirmSub = true
      this.showPop = true
    }
  },
  mounted () {
    fetch(`/api/examination/${this.eid}?format=json`)
      .then(res => res.json())
      .then(({ id, duration, questions, num_questions }) => {
        this.questions = questions
        this.numQuestions = num_questions
        this.duration = Number(duration)
        this.currentQuestion = 0
        this.answered = 0
        const answers = questions.map(q => ({ question_id: q.id, selected_option: null }))
        this.answerSheet = {
          answers,
          examination_id: id,
          student_id: this.sid
        }
        this.confirmSub = false
        this.popText = this.popTexts[0]
        this.notStarted = true
        this.ongoing = false
      })

  }
})