import React from 'react'
import axios from "axios";
import './Character.css'
import configData from "../../configFile.json";

export default class Character extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            isOutside: false,
            blocks: [
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            ],
            error: null
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
    }


    componentWillUnmount() {
    }

    equipItem(item, position)
    {
        axios.post(location.protocol + configData.SERVER_URL + 'inventory', item).then (res => {
            console.log(res);
            this.state.blocks[position - 1] = "+"
            this.forceUpdate()
        });
    }

    dropHandler(e, mainCategory, subCategory, position) {
        console.log("Handler")
        if (!this.state.isOutside) {
            let data = e.dataTransfer.getData("item");
            var obj = JSON.parse(data)
            console.log(mainCategory, obj.mainCategoryName)
            console.log(subCategory, obj.subCategoryName)
            if (mainCategory === obj.mainCategoryName &&
                subCategory === obj.subCategoryName) {
                obj['position'] = position
                this.equipItem(obj, position)
                console.log("ASDADASD")
                console.log(obj)
            }
            return undefined;
        }
        else
        {
            this.state.blocks[position - 1] = ""
            this.forceUpdate()
        }

    }

    dragEnterHandler(e) {
        this.setState({isOutside: false})
        return undefined;
    }

    dragLeaveHandler(e) {
        console.log("Leave")
        this.setState({isOutside: true})
        return undefined;
    }

    dragEndHandler(e, position) {
        console.log("END")
        this.state.blocks[position - 1] = ""
        this.forceUpdate()
        e.stopPropagation();
        e.preventDefault();
        return undefined;
        }


    render() {

        function dragOverHandler(e) {
            e.stopPropagation();
            e.preventDefault();
            return undefined;
        }

        return (
            <div className="CharacterBlock">
                <div className="DropableBlocks">
                    <div className="LeftBlocks">
                        <div id="head" className="Block" draggable={true}
                                onDragEnter={(e) => this.dragEnterHandler(e)}
                                onDragLeave={(e) => this.dragLeaveHandler(e)}

                                onDragEnd={(e) => this.dragEndHandler(e, 1)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда","Голова", 1)}>
                            {this.state.blocks[0]}
                        </div>

                        <div id="body" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 3)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда", "Тело", 3)}>
                            {this.state.blocks[2]}
                        </div>

                        <div id="leftHand" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 5)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Оружие", "Левая рука", 5)}>
                            {this.state.blocks[4]}
                        </div>
                        <div id="shoes" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 7)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда", "Обувь", 7)}>
                            {this.state.blocks[6]}
                        </div>

                    </div>
                    <div className="RightBlocks">
                        <div id="neck" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e,2 )}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда", "Шея", 2)}>
                            {this.state.blocks[1]}
                        </div>
                        <div id="hands" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 4)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда", "Руки", 4)}>
                            {this.state.blocks[3]}
                        </div>
                        <div id="rightHand" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 6)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Оружие", "Правая рука", 6)}>
                            {this.state.blocks[5]}
                        </div>
                        <div id="legs" className="Block"
                                onDragEnd={(e) => this.dragEndHandler(e, 8)}
                                onDragOver={(e) => dragOverHandler(e)}
                                onDrop={(e) => this.dropHandler(e, "Одежда", "Ноги", 8)}>
                            {this.state.blocks[7]}
                        </div>
                    </div>
                </div>
                <div className="Character">
                </div>
            </div>
        )
    }
}