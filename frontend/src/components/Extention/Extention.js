import React from 'react'

import './Extention.css'
import TabPane from "./Tab-pane";
import Tabs from "./Tabs";
import Statistic from "../Statistic/Statistic";
import axios from "axios";
import configData from "../../configFile.json";
import HeaderComponent from "../HeaderComponent/HeaderComponent";
import Actions from "../Actions/Actions";

export default class App extends React.Component{
    constructor(props){
        super(props)
        this.state = {
          error: null
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
    }


    componentWillUnmount(){
    }
    
    render(){
        return (
            <div className="main_window background">
                <div className="extention">
                    <HeaderComponent />
                    <div className="container">
                        <Tabs>
                            <TabPane name="Статистика" key="1">
                                <Statistic user={this.state.user}/>
                            </TabPane>
                            <TabPane name="Действия" key="2">
                                <Actions />
                            </TabPane>
                            <TabPane name="Инвентарь" key="3">
                                Content of Tab Pane 2
                            </TabPane>
                            <TabPane name="Рейды" key="4">
                                Content of Tab Pane 3
                            </TabPane>
                        </Tabs>
                    </div>
                </div>
            </div>
        )
    }
}