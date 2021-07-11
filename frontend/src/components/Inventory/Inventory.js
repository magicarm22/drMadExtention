import React from 'react'
import axios from "axios";
import configData from "../../configFile.json";

export default class Inventory extends React.Component{
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

    componentDidMount(){
        this.getInventory()
        this.interval = setInterval(() =>
        this.getInventory(), 10000);
    }

    getInventory()
    {
        axios.get(location.protocol + configData.SERVER_URL + 'inventory').then (res => {
            console.log(res)
            this.setState({ inventory: res.data, isLoaded: true });

        });

    }


    componentWillUnmount(){
        clearInterval(this.interval);
    }


    render(){
        function dragStartHandler(e, item) {
            console.log('start drag')
            console.log(item)
            e.dataTransfer.effectAllowed = "copyMove";
            var strItem = JSON.stringify(item);
            e.dataTransfer.setData('item', strItem)
            return undefined;
        }

        function dragLeaveHandler(e) {
            return undefined;
        }

        function dragEndHandler(e) {
            return undefined;
        }

        function dragOverHandler(e) {
            return undefined;
        }

        function dropHandler(e, item) {
            console.log(item)
            return undefined;
        }

        if (this.state.isLoaded) {
            return (
                <div className="Inventory">
                    <div className="Welcome">
                        Ваши предметы
                    </div>
                    <div className="yourItems">
                        {this.state.inventory.map((item, index) => (
                            <div key={index}
                                onDragStart={(e) => dragStartHandler(e, item)}
                                onDragLeave={(e) => dragLeaveHandler(e)}
                                onDragEnd={(e) => dragEndHandler(e)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => dropHandler(e, item)}
                                draggable={true}>
                                {item.itemName}
                            </div>
                        ))}
                    </div>
                </div>
            )
        }
        else
        {
            return (
                <div className="Inventory">
                    Loading...
                </div>
            )
        }
    }
}