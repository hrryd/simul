import React, { Component } from 'react';
import { Table } from 'antd';
var dateFormat = require('dateformat');

const URL = 'ws://localhost:31234/api/ws';

class Log extends Component {

    state = {
        messages: [] //this.testData()
    }

    ws = new WebSocket(URL);

    testData() {
        let messages = [];
        let messagesPerSecond = 200;
        let nodes = 5;
        let duration = 60;
        let startTime = Date.now();
        let key = 0;

        for (let i = 0; i < duration * messagesPerSecond; i++) {
            for (let n = 0; n < nodes; n++) {
                let timestamp = new Date(startTime - Math.round(Math.random() * duration * 1000)).getTime();
                messages.push({key: key++, timestamp: timestamp, node: `app-${n}`, msg: 'xyz'})
            }
        }
        return messages;
    }

    addMessage(message) {
        message.key = this.state.messages.length;
        this.setState(state => ({ messages: [message, ...state.messages]}));
    }

    componentDidMount() {
        this.ws.onopen = () => {
            console.debug('connected');
        }
      
        this.ws.onmessage = evt => {
            const msgs = JSON.parse(evt.data);
            console.debug(msgs);
            msgs.forEach(msg => {
                this.addMessage(msg);
            });
        }
      
          this.ws.onclose = () => {
            console.debug('disconnected');
            this.setState({
              ws: new WebSocket(URL),
            });
          };
    }
    

    render() {   
        const columns = [
            {
                title: 'Timestamp',
                dataIndex: 'timestamp',
                width: 175,
                render: (t, r, i) => dateFormat(new Date(parseInt(r.timestamp)), "H:MM:ss.l"),
                defaultSortOrder: 'descend',
                sorter: (a, b) => a.timestamp - b.timestamp,
            },
            {
                title: 'Node',
                dataIndex: 'node',
                width: 175,
                filters: [
                    {
                        text: 'app-0',
                        value: 'app-0'
                    },
                    {
                        text: 'app-1',
                        value: 'app-1'
                    },
                    {
                        text: 'app-2',
                        value: 'app-2'
                    }
                ],
                onFilter: (value, record) => record.node === value,
            },
            {
                title: 'Output',
                dataIndex: 'msg',
            },
        ];

        return (
            <div>
                <Table dataSource={this.state.messages} columns={columns} pagination={{ pageSize: 50 }} />
            </div>
        )
    }

}

export default Log;