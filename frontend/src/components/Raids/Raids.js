import React from "react";
import axios from "axios";
import configData from "../../configFile.json";
import Table from "@material-ui/core/Table";
import TableRow from "@material-ui/core/TableRow";
import TableHead from "@material-ui/core/TableHead";
import TableContainer from "@material-ui/core/TableContainer";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import './Raids.css'
import InRaid from "../InRaid/InRaid";


export default class Raids extends React.Component {


    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
            raids: [],
            isInRaid: false
        };
        this.maxPlayers = 4
    }

    contextUpdate(context, delta) {
        if (delta.includes('theme')) {
            this.setState(() => {
                return {theme: context.theme}
            })
        }
    }

    componentDidMount() {
        this.getCreatedRaids()
        this.interval = setInterval(() =>
        this.getCreatedRaids(), 10000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    getCreatedRaids()
    {
         axios.get(location.protocol + configData.SERVER_URL + 'raids').then (res => {
            console.log(res)
             this.setState({isLoaded: true, raids: res.data})
         });
    }

    handleClick(row,column,event) {
        if (row.countPlayer + 1 > this.maxPlayers)
            return
        this.joinRaid(row.raidid)

    }

    joinRaid(raidid) {
        axios.post(location.protocol + configData.SERVER_URL + 'raids', {'partyid': raidid}).then (res => {
            console.log(res)
            // this.getCreatedRaids()
            this.setState({isInRaid: true})
         });
    }

    render() {
        const {isLoaded, raids, isInRaid} = this.state;
        if (this.state.isLoaded) {
            return (
                <div className="raids">
                    {isInRaid && <InRaid />}
                    {!isInRaid &&
                        <TableContainer>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell className="TableRaidsHeader" width="5px" align="center">#</TableCell>
                                        <TableCell align="center" width="10px"
                                                   className="TableRaidsHeader">Количество</TableCell>
                                        <TableCell align="center" className="TableRaidsHeader">Команда</TableCell>
                                        <TableCell align="center" className="TableRaidsHeader">Локация</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {this.state.raids.filter((row, index) => row.isRaidStarted === false).map((row, index) => (
                                        <TableRow onClick={(e) => this.handleClick(row, index, e)}>
                                            <TableCell className="TableRaidsBody" width="5px">{index + 1}</TableCell>
                                            <TableCell className="TableRaidsBody"
                                                       width="10px">{row.countPlayer}/{this.maxPlayers}</TableCell>
                                            <TableCell
                                                className="TableRaidsBody">{[row['player1'], row['player2'], row['player3'], row['player4']].filter(Boolean).join(', ')}</TableCell>
                                            <TableCell className="TableRaidsBody">{row.location}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    }
                </div>
            )
        }
        else {
            return ("Loading...")
        }
    }
}