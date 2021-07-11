import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class Shop extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            isLoaded: false,
            shop: null,
            errorMessage: ""
        };
    }

    contextUpdate(context, delta){
        if(delta.includes('theme')){
            this.setState(()=>{
                return {theme:context.theme}
            })
        }
    }

    getShop(){
        axios.get(location.protocol + configData.SERVER_URL + 'shop').then (res => {
            this.setState({ shop: res.data, isLoaded: true })});
    }

    buyItem(itemId){
        console.log(itemId)
        axios.post(location.protocol + configData.SERVER_URL + 'shop', {
            "itemId": itemId
        }, { validateStatus: false }).then (res => {
            console.log(res)
            if (res.status === 200 && res.data["errorCode"] === 0) {
                this.getShop();
            }
            else if (res.status === 404 && res.data["errorCode"] === 1)
            {
                this.setState({errorMessage: "Простите, это какая-то магия. Я не могу продать вам этот предмет. Может, еще раз?"})
            }
            else if (res.status === 404 && res.data["errorCode"] === 2)
            {
                this.setState({errorMessage: "Только что какой-то больной пришел и забрал этот товар! Может, вы выберете что-то еще?"})
                this.getShop();
            }
            else if (res.status === 404 && res.data["errorCode"] === 3)
            {
                this.setState({errorMessage: "Раз пилюля, два пилюля... И это все? Нееее, так дело не пойдет!"})
            }
        })
    }

    componentDidMount() {
        this.getShop()
        this.interval = setInterval(() =>
        this.getShop(), 10000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }


    render(){
        if (this.state.isLoaded) {
            console.log(this.state.shop.items)
            return (
                <div className="Shop">
                    <div className="Welcome">
                        Добро пожаловать в магазин. Вот, что у нас есть!
                    </div>
                    <div className="Items">
                        {this.state.shop.items.map((item, index) => (
                            <li key={index}><button onClick={() => this.buyItem(item.itemId)}>{item.itemName}</button></li>
                              ))}
                    </div>
                    <div className="errorBlock">
                        {this.state.errorMessage}
                    </div>
                </div>
            )
        }
        else {
            return (
                <div className="Shop">
                    Loading...
                </div>
            )
        }
    }
}