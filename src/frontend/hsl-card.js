import {
  LitElement, html, svg
} from 'https://unpkg.com/@polymer/lit-element@^0.6.3/lit-element.js?module';

class HSLCard extends LitElement {

  static get properties() {
    return {
      _hass: Object,
      config: Object,
    }
  }

  set hass(hass) {
     this._hass = hass;

     }

  setConfig(config) {
      if (!config.entity) {
        throw new Error('You need to define an entity');
      }
      this.config = config;
    }

  getCardSize() {
      return 1;
  }

  render({hass,  config } = this) {
    console.log("rencder HSL card A");
    const now = new Date();

    const entityId = this.config.entity;
    const state = this._hass.states[entityId];

    const nextDeparture = state ? new Date(state.state) : 'unavailable';
    var m = moment(nextDeparture)
    var timeTillNextDeparture = m.fromNow();
    var route = state["attributes"]["route"];
    var timestring = m.format("HH:mm")
    console.log(entityId, state, timeTillNextDeparture)
    console.log("rencder HSL card B");

    return html`
      <style>
      .hsl-card{
        padding: 10px;
        background-color: #007ac9;
        color: white;

      }
      .logo{
        vertical-align: middle;
        padding-right: 15px;
      }
      .route {
        font-size: x-large;
        vertical-align: middle;
        padding-right: 15px;
      }
      .time {

        vertical-align: middle;
        font-size: x-large;
        font-weight: bold;


      }
      .abs_time {
        vertical-align: middle;
        font-size: x-small;
      }
      </style>
      <ha-card >
      <div class="hsl-card">
        <img class="logo" width="50px" src="/local/hsl_logo.png"></img><ha-icon icon="mdi:bus"></ha-icon><span class="route">${route}</span>
        <span class="time"> ${timeTillNextDeparture}</span>
        <span class="abs_time">(${timestring})</span>
      </div>
      </ha-card>
      `;

  }



}

customElements.define('hsl-card', HSLCard);
