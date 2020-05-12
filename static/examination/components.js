Vue.component('timer', {
  data () {
    return {
      timeLeft: "00:00:00"
    }
  },
  template: `<span id="timer">{{ timeLeft }}</span>`,
  props: ['hours', 'callback'],
  mounted () {
    this.countdown()
  },
  methods: {
    countdown () {
      let secs = Math.floor(this.hours * 3600)
      const inte = setInterval(() => {
        if (secs === 0) {
          this.callback()
          clearInterval(inte)
        } else {
          secs--
          this.timeLeft = this.getTimeString(secs)
        }
      }, 1000)
    },
    getTimeString (secs) {
      const tformat = (t) => String(t).padStart(2, '0')
      const hours = Math.floor(secs / 3600)
      secs -= hours * 3600
      const mins = Math.floor(secs / 60)
      secs -= mins * 60
      return `${tformat(hours)}:${tformat(mins)}:${tformat(secs)}`
    }
  }
})

Vue.component('question', {
  props: ['question', 'number'],
  template: `
    <div class='question'>
      <div class='qnumber'>{{ number }}</div>
      <div class='content'>{{ question.content }}</div>
      <ul class='options'>
        <li
          v-for='(option, i) in question.options'
          :class='{option: true, selected: option.id == selectedOption}'
          :key='option.id'
          @click='select(option.id)'
        >
        <span class="option-s">{{ alphabet[i] }}.</span>
        {{ option.option_content }}
        </li>
      </ul>
    </div>
  `,
  data () {
    return {
      selectedOption: null,
      alphabet: 'abcdefghijklmnopqrstuvwxyz'
    }
  },
  methods: {
    select (option) {
      this.selectedOption = option
      this.$emit('select-option', option)
    }
  }
})