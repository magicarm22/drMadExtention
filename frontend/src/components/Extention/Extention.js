import React from 'react'

import './Extention.css'
import TabPane from "./Tab-pane";
import Tabs from "./Tabs";
import Statistic from "../Statistic/Statistic";
import axios from "axios";
import configData from "../../configFile.json";
import Grid from "@material-ui/core/Grid";
import HeaderComponent from "../HeaderComponent/HeaderComponent";
import Actions from "../Actions/Actions";
import Shop from "../Shop/Shop";
import Inventory from "../Inventory/Inventory";
import Character from "../Character/Character";
import {Button} from "@material-ui/core";
import Buttons from "../Buttons/Buttons";
import Raids from "../Raids/Raids";
import Injection from "../Injection/Injection";

export default class App extends React.Component{
    constructor(props){
        super(props)
        this.state = {
          showInjection: false,
          showShop: false,
          showRaids: false,
          showStats: false,
          showPack: false,
          showTrade: false,
          showHelp: false,
          showButtons: true
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
        axios.get(location.protocol + configData.SERVER_URL + 'info').then(r => null)
    }

    updateState = (newState) => {
        console.log(newState)
        this.setState(newState);
    }

    componentWillUnmount(){
    }
    
    render(){
        const { showInjection, showShop, showRaids, showStats, showPack, showTrade, showHelp, showButtons} = this.state;
        return (
            <div className="main_window background">
                <div className="extention">
                    <HeaderComponent />
                    <Character />
                    {showInjection && <Injection />}
                    {showShop && <Shop />}
                    {showRaids && <Raids />}
                    {showStats && <Statistic />}
                    {showPack && <Inventory />}
                    {/*{showTrade && <>}*/}
                    {/*{showHelp && </>}*/}
                    {showButtons && <Buttons changeComponent={this.updateState}/>}
                        {/*<Tabs>*/}
                        {/*    <TabPane name="Статистика" key="1">*/}
                        {/*        <Statistic user={this.state.user}/>*/}
                        {/*    </TabPane>*/}
                        {/*    <TabPane name="Действия" key="2">*/}
                        {/*        <Actions />*/}
                        {/*    </TabPane>*/}
                        {/*    <TabPane name="Инвентарь" key="3">*/}
                        {/*        <Inventory />*/}
                        {/*    </TabPane>*/}
                        {/*    <TabPane name="Рейды" key="4">*/}
                        {/*        Content of Tab Pane 3*/}
                        {/*    </TabPane>*/}
                        {/*    <TabPane name="Магазин" key="5">*/}
                        {/*        <Shop />*/}
                        {/*    </TabPane>*/}
                        {/*</Tabs>*/}
                </div>
            </div>
        )
    }
}