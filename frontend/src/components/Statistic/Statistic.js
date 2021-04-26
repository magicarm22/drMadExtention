import React from "react";
import axios from "axios";
import configData from "../../configFile.json";

export default class Statistic extends React.Component {


    constructor(props) {
        super(props)
        this.state = {
          user: null,
          isLoaded: false,
          error: null,
        };
    }

    contextUpdate(context, delta) {
        if (delta.includes('theme')) {
            this.setState(() => {
                return {theme: context.theme}
            })
        }
    }

    componentDidMount() {
        axios.get(location.protocol + configData.SERVER_URL + 'info').then (res => {
            this.setState({ user: res.data, isLoaded: true });
        })
    }

    componentWillUnmount() {
    }

    render() {
        if (this.state.isLoaded) {
            return (
                <div className="statistic">
                    Имя: {this.state.user.nickname} <br />
                    Количество рейдов: {this.state.user.countRaids} раз <br />
                    Количество выписок: {this.state.user.countCerts} раз <br />
                    Количество таблеток: {this.state.user.pills} шт. <br />
                    Показатель атаки: {this.state.user.pa} <br />
                    Показатель защиты: {this.state.user.pz} <br />
                    Показатель удачи: {this.state.user.py} <br />
                </div>
            )
        }
        else {
            return (<div className="statistic">
                        Loading...
                    </div>
            )
        }
    }
}