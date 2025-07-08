(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[63642],{80087:function(e,t,o){Promise.resolve().then(o.bind(o,49352)),Promise.resolve().then(o.bind(o,60881)),Promise.resolve().then(o.bind(o,32810)),Promise.resolve().then(o.bind(o,85337)),Promise.resolve().then(o.bind(o,13162)),Promise.resolve().then(o.bind(o,22376)),Promise.resolve().then(o.bind(o,49421)),Promise.resolve().then(o.bind(o,89026))},69583:function(e,t,o){var n=o(92244),i=o(35147);e.exports=function(e,t){return e&&n(e,t,i)}},20993:function(e,t,o){var n=o(16610),i=o(69583),l=o(60876);e.exports=function(e,t){var o={};return t=l(t,3),i(e,function(e,i,l){n(o,i,t(e,i,l))}),o}},14892:function(e,t,o){"use strict";var n=o(20993),i=o.n(n),l=o(21125);let a=e=>i()(e,e=>"string"==typeof e?(0,l.Z)(e).trim():e);t.Z=(e,t,o,n={})=>({id:e.toLowerCase().replace(/\s/g,"-"),props:a(t),banner:n.banner,codeBanner:n.codeBanner,wrapper:n.wrapper,nonConsoleExample:n.nonConsoleExample,title:e,definition:o})},32810:function(e,t,o){"use strict";o.d(t,{ComponentSnippet:function(){return s}});var n=o(27573),i=o(11568),l=o(62483),a=o(63343),m=o(66833);function s(){let{source:e,loading:t,Component:o}=(0,m.Z)({showCode:!0,showDemo:!0,identifier:"attribute-editor"});return(0,n.jsxs)(i.Z,{loading:t,description:"",title:"Attribute editor",snippet:e,children:[(0,n.jsx)(l.Z,{margin:{bottom:"m"},children:(0,n.jsx)(o,{})}),(0,n.jsx)(a.Z,{statusIconAriaLabel:"Info",children:"This example showcases how to wire your code with add/remove/input events and update application state."})]})}},89026:function(e,t,o){"use strict";var n=o(27573);o(7653);var i=o(63343),l=o(59639),a=o(14892);let m=function(e,t){let o={props:{onAddButtonClick:{value:"() => setItems([...items, {}])",type:l.Z.Function},onRemoveButtonClick:{value:`
        ({ detail: { itemIndex } }) => {
          const tmpItems = [...items];
          tmpItems.splice(itemIndex, 1);
          setItems(tmpItems);
        }
        `,type:l.Z.Function},items:{value:[],type:l.Z.Array,stateful:!0},gridLayout:{value:""},customRowActions:{type:l.Z.Object}}};return(0,a.Z)(e,t,o,{banner:(0,n.jsx)(i.Z,{statusIconAriaLabel:"Info",children:"This example makes use of controlled components. We have omitted the corresponding change handlers to keep the code sample simple. Editing these fields will not work. Adding and removing rows will work."})})},s=[m("Default",{empty:"No items associated with the resource.",addButtonText:"Add new item",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key" />
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value" />
          }
        ]
        `}),m("Empty state",{addButtonText:"Add new item",empty:"No items associated with the resource.",items:[],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key"/>
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value"/>
          }
        ]`}),m("With info links",{addButtonText:"Add new item",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key"/>,
            info: <Link variant="info">Info</Link>
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value"/>,
            info: <Link variant="info">Info</Link>
          }
        ]
        `}),m("With constraint text",{addButtonText:"Add new item",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key"/>
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value"/>,
            constraintText: (item, index) => index === items.length - 1 ? 'Constraint text for the last value' : null
          }
        ]
        `}),m("With limit",{addButtonText:"Add new item",additionalInfo:"<span>You can add up to {50 - items.length} more items.</span>",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key"/>
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value"/>
          }
        ]
        `}),m("With limit reached",{addButtonText:"Add new item",disableAddButton:!0,additionalInfo:"You have reached the limit of 50 items.",empty:"No items associated with the resource.",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key"/>
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value"/>
          }
        ]`}),m("With different control types",{addButtonText:"Add new item",items:[{key:"some-key-1",value:"some-value-1",type:{label:"Type 1",value:"0"}},{key:"some-key-2",value:"some-value-2",type:{label:"Type 2",value:"1"}}],definition:`
          [
            {
              label: "Key",
              control: item => <Input value={item.key} placeholder="Enter key" />
            },
            {
              label: "Value",
              control: item => <Input value={item.value} placeholder="Enter value" />,
              warningText: (item, index) => index === 1 ? "Warning message": null
            },
            {
              label: "Type",
              control: item =>
                <Select
                  selectedOption={item.type}
                  options={[
                    {
                      label: "Type 1",
                      value: "0"
                    },
                    {
                      label: "Type 2",
                      value: "1"
                    }
                  ]}
                />,
              errorText: (item, index) => index === 1 ? "Error message": null
            }
          ]
          `}),m("Custom row actions",{empty:"No items associated with the resource.",addButtonText:"Add new item",items:[{key:"some-key-1",value:"some-value-1"},{key:"some-key-2",value:"some-value-2"}],definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key" />
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value" />
          }
        ]
        `,customRowActions:`
        ({ itemIndex }) => {
          const onClick = ({ detail: { id } }) => {
            const tmpItems = [...items];
            const item = tmpItems[itemIndex];
            switch (id) {
              case 'move-up':
                tmpItems[itemIndex] = tmpItems[itemIndex - 1];
                tmpItems[itemIndex - 1] = item;
                break;
              case 'move-down':
                tmpItems[itemIndex] = tmpItems[itemIndex + 1];
                tmpItems[itemIndex + 1] = item;
                break;
            }
            setItems(tmpItems);
          }
          return (
            <ButtonDropdown
              items={[
                { text: 'Move up', id: 'move-up' },
                { text: 'Move down', id: 'move-down' }
              ]}
              ariaLabel={\`Remove item \${itemIndex+1}\`}
              mainAction={{
                text: 'Remove',
                onClick: () => {
                  const tmpItems = [...items];
                  tmpItems.splice(itemIndex, 1);
                  setItems(tmpItems);
                }
              }}
              onItemClick={onClick}
            />
          );
        }
        `}),m("Flexible layout",{empty:"No items associated with the resource.",addButtonText:"Add new item",items:`[
      {
        key: 'key-1',
        option: {
          label: 'Option 1', value: '1'
        },
        value: 'some-value-1',
        value2: {
          type: "absolute",
          startDate: "2024-01-09T12:34:56",
          endDate: "2024-01-19T15:30:00"
        },
      },
      {
        key: 'key-2',
        option: {
          label: 'Option 2', value: '2'
        },
        value: 'some-value-2',
        value2: {
          type: "relative",
          amount: 12,
          unit: "day"
        }
      },
    ]`,definition:`
        [
          {
            label: "Key",
            control: item => <Input value={item.key} placeholder="Enter key" />
          },
          {
            label: "Value",
            control: item => <Input value={item.value} placeholder="Enter value" />
          },
          {
            label: "Longer value",
            control: item => <DateRangePicker
              value={item.value2}
              placeholder="Filter by a date and time range"
            />
          }
        ]
        `,gridLayout:`[
    {
      rows: [
        [1, 2, 4]
      ],
      removeButton: {
        ownRow: false,
        width: 'auto'
      },
      breakpoint: 's'
    },
    {
      rows: [
        [1, 2, 4]
      ],
      removeButton: {
        ownRow: true,
        width: 'auto'
      },
      breakpoint: 'xs'
    },
    {
      rows: [
        [1, 2],
        [4]
      ],
      breakpoint: 'xxs'
    },
    {
      rows: [
        [1],
        [1],
        [1],
      ]
    }
  ]`})];t.default=s},59639:function(e,t){"use strict";t.Z={String:"string",ReactNode:"react node",Boolean:"boolean",Number:"number",Enum:"enum",Array:"array",Object:"object",Function:"function",Ref:"ref",Date:"date",Custom:"custom"}}},function(e){e.O(0,[81241,47439,81543,76075,46334,38517,53501,93241,60380,25205,12334,62256,99897,67036,12147,96286,42542,53309,15850,80543,27215,37804,90595,63561,91917,17773,74318,30628,93475,2315,4202,19164,62152,50590,71052,39145,30097,74736,95664,92086,73580,44645,83462,24159,58886,86310,68313,50865,12701,99236,58986,52269,96623,15935,43927,6377,21799,28666,80573,17015,54884,71093,11093,44570,61119,60103,63253,70718,63343,32108,54299,90425,58982,90975,15109,82277,87376,88616,5114,77343,19404,50294,48557,87639,60697,614,1438,54039,81293,1528,1744],function(){return e(e.s=80087)}),_N_E=e.O()}]);