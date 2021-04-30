import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class Shop extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            isLoaded: false
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
                    <div className="Предметы">
                        {this.state.shop.items.map((item) => (
                                <li>{item.itemName}</li>
                              ))}
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