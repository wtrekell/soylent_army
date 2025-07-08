(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4005],{57564:function(e,t,n){Promise.resolve().then(n.bind(n,49352)),Promise.resolve().then(n.bind(n,60881)),Promise.resolve().then(n.bind(n,85337)),Promise.resolve().then(n.bind(n,13162)),Promise.resolve().then(n.bind(n,22376)),Promise.resolve().then(n.bind(n,49421)),Promise.resolve().then(n.bind(n,86080))},69583:function(e,t,n){var i=n(92244),o=n(35147);e.exports=function(e,t){return e&&i(e,t,o)}},20993:function(e,t,n){var i=n(16610),o=n(69583),r=n(60876);e.exports=function(e,t){var n={};return t=r(t,3),o(e,function(e,o,r){i(n,o,t(e,o,r))}),n}},14892:function(e,t,n){"use strict";var i=n(20993),o=n.n(i),r=n(21125);let a=e=>o()(e,e=>"string"==typeof e?(0,r.Z)(e).trim():e);t.Z=(e,t,n,i={})=>({id:e.toLowerCase().replace(/\s/g,"-"),props:a(t),banner:i.banner,codeBanner:i.codeBanner,wrapper:i.wrapper,nonConsoleExample:i.nonConsoleExample,title:e,definition:n})},86080:function(e,t,n){"use strict";var i=n(27573),o=n(7653),r=n(14892),a=n(45001),s=n(25505),d=n(63343);let c=e=>`<Board 
  items={[{ id: '1', rowSpan: ${e}, columnSpan: 4, data: {}}]}
  renderItem={() => <BoardItem />}
  i18nStrings={${s.CX}}
  onItemsChange={() => {}}
/>`,l=`<ItemsPalette 
  items={[{ id: '1', data: {}}]}
  renderItem={() => <BoardItem />}
  i18nStrings={${s.kh}}
/>`,m=()=>{let e=(0,o.useContext)(a.xD);return(0,i.jsxs)(d.Z,{statusIconAriaLabel:"Info",children:["This example is static. Resizing and moving the item does not work in this preview. You can see it in action on the ",(0,i.jsx)(e,{to:"/examples/react/configurable-dashboard.html",children:"configurable dashboard demo"}),"."]})},u=function(e,{wrapper:t=c(2)},n){return(0,r.Z)(e,{i18nStrings:s.Rh,...n},void 0,{banner:(0,i.jsx)(m,{}),wrapper:t})},p=JSON.stringify(new Date().toLocaleDateString("en-US",{year:"numeric",month:"long"})),v=`
<div style={{ maxWidth: 280 }}>
  <FormField label="Filter displayed data">
    <Select
      selectedOption={{ value: ${p} }}
      empty="Not supported in this demo"
    />
  </FormField>
</div>
<ColumnLayout columns={2} variant="text-grid">
  <div>
    <Header variant="h3">Overview</Header>
    <SpaceBetween size="s">
      <KeyValuePairs
        columns={1}
        items={[
          {
            label: 'Status',
            value: <StatusIndicator type="success">Service is operating normally</StatusIndicator>,
          },
          {
            label: 'Enabled Regions',
            value: '10',
          },
          {
            label: 'Instances',
            value: '18 in 10 regions',
          },
          {
            label: 'Security groups',
            value: '11 in 10 regions',
          },
          {
            label: 'Volumes',
            value: '34 in 10 regions',
          }
        ]} 
      />
    </SpaceBetween>
  </div>
  <div>
    <Header variant="h3">Breakdown</Header>
    <BarChart
      hideFilter={true}
      hideLegend={true}
      xScaleType="categorical"
      xTitle="Chars"
      yTitle="Numbers"
      series={[{
        type: 'bar',
        title: 'Value',
        data: [
          { x: 'A', y: 170.25 },
          { x: 'B', y: 116.07 },
          { x: 'C', y: 54.19 },
          { x: 'D', y: 15.18 },
          { x: 'E', y: 15.03 },
          { x: 'F', y: 49.85 },
        ],
      }]}
      height={230}
    />
  </div>
</ColumnLayout>`,h=[u("Simple",{},{header:"<Header>Board item title</Header>",children:"Board item content",footer:"Board item footer"}),u("With actions",{},{header:`<Header 
  description="Board item description" 
  actions={<Button iconAlign="right" iconName="external">View in console</Button>}
>Board item title</Header>`,children:"Board item content",settings:`<ButtonDropdown
  items={[
    { id: 'preferences', text: 'Preferences' },
    { id: 'remove', text: 'Remove' }
  ]}
  ariaLabel="Board item settings"
  variant="icon"
/>`}),u("With table",{wrapper:c(4)},{header:"<Header>Board item title</Header>",footer:'<Box textAlign="center"><Link>View all</Link></Box>',disableContentPaddings:!1,children:`<div style={{ overflow: "hidden" }}>
    <Table
      variant="embedded"
      columnDefinitions={[
        { header: "ID", cell: (item) => <Link href="#">{item.id}</Link> },
        { header: "Status", cell: (item) => <StatusIndicator type={item.status.toLowerCase()}>{item.status}</StatusIndicator> },
      ]}
      items={[
        { id: "6f80c977-ca20-4563-8007-6387581f9a34", status: "Success" },
        { id: "4345032a-e270-4e6f-a187-60bf7ddd4ba3", status: "Success" },
        { id: "54dc6682-26d0-4c70-a42a-1772d443dd0d", status: "Success" },
        { id: "bcd939ad-2203-4585-8e93-d944632872ef", status: "Error" },
        { id: "244d0a59-c18d-4c18-90c2-deba14535d51", status: "Success" },
        { id: "bcd939ad-2203-4585-8e93-d944632872ef", status: "Pending" },
      ]}
    />
  </div>`,settings:`<ButtonDropdown
  items={[
    { id: 'preferences', text: 'Preferences' },
    { id: 'remove', text: 'Remove' }
  ]}
  ariaLabel="Board item settings"
  variant="icon"
/>`}),u("With mixed content",{wrapper:c(5)},{header:"<Header>Board item with mixed content types</Header>",settings:`<ButtonDropdown
  items={[{ id: 'remove', text: 'Remove' }]}
  ariaLabel="Board item settings"
  variant="icon"
/>`,footer:'<Box textAlign="center"><Link>View all</Link></Box>',children:v}),u("Palette item",{wrapper:l},{header:"<Header>Board item in palette</Header>",children:`<div style={{ display: 'flex',  alignItems: 'center', gap: 10 }}>
    <img src="/preview-cube.svg" alt="cube icon" />
    <p>Palette item description</p>
</div>`})];t.default=h},25505:function(e,t,n){"use strict";n.d(t,{CX:function(){return i},Rh:function(){return o},kh:function(){return r}});let i=`(() => {
  function createAnnouncement(operationAnnouncement, conflicts, disturbed) {
    const conflictsAnnouncement =
      conflicts.length > 0 ? \`Conflicts with $\{conflicts.map(c => c.data.title).join(', ')}.\` : '';
    const disturbedAnnouncement = disturbed.length > 0 ? \`Disturbed $\{disturbed.length} items.\` : '';
    return [operationAnnouncement, conflictsAnnouncement, disturbedAnnouncement].filter(Boolean).join(' ');
  }
  return {
    liveAnnouncementDndStarted: operationType => (operationType === 'resize' ? 'Resizing' : 'Dragging'),
    liveAnnouncementDndItemReordered: operation => {
      const columns = \`column $\{operation.placement.x + 1}\`;
      const rows = \`row $\{operation.placement.y + 1}\`;
      return createAnnouncement(
        \`Item moved to $\{operation.direction === 'horizontal' ? columns : rows}.\`,
        operation.conflicts,
        operation.disturbed
      );
    },
    liveAnnouncementDndItemResized: operation => {
      const columnsConstraint = operation.isMinimalColumnsReached ? ' (minimal)' : '';
      const rowsConstraint = operation.isMinimalRowsReached ? ' (minimal)' : '';
      const sizeAnnouncement =
        operation.direction === 'horizontal'
          ? \`columns $\{operation.placement.width}$\{columnsConstraint}\`
          : \`rows $\{operation.placement.height}$\{rowsConstraint}\`;
      return createAnnouncement(\`Item resized to $\{sizeAnnouncement}.\`, operation.conflicts, operation.disturbed);
    },
    liveAnnouncementDndItemInserted: operation => {
      const columns = \`column $\{operation.placement.x + 1}\`;
      const rows = \`row $\{operation.placement.y + 1}\`;
      return createAnnouncement(\`Item inserted to $\{columns}, $\{rows}.\`, operation.conflicts, operation.disturbed);
    },
    liveAnnouncementDndCommitted: operationType => \`$\{operationType} committed\`,
    liveAnnouncementDndDiscarded: operationType => \`$\{operationType} discarded\`,
    liveAnnouncementItemRemoved: op => createAnnouncement(\`Removed item $\{op.item.data.title}.\`, [], op.disturbed),
    navigationAriaLabel: 'Board navigation',
    navigationAriaDescription: 'Click on non-empty item to move focus over',
    navigationItemAriaLabel: item => (item ? item.data.title : 'Empty'),
  };
})()`,o=`{
  dragHandleAriaLabel: 'Drag handle',
  dragHandleAriaDescription:
    'Use Space or Enter to activate drag, arrow keys to move, Space or Enter to submit, or Escape to discard. Be sure to temporarily disable any screen reader navigation feature that may interfere with the functionality of the arrow keys.',
  resizeHandleAriaLabel: 'Resize handle',
  resizeHandleAriaDescription:
    'Use Space or Enter to activate resize, arrow keys to move, Space or Enter to submit, or Escape to discard. Be sure to temporarily disable any screen reader navigation feature that may interfere with the functionality of the arrow keys.',
}`,r=`{
  navigationAriaLabel: 'Items palette navigation',
  navigationAriaDescription: 'Click on an item to move focus over',
  navigationItemAriaLabel: item => item.data.title,
  liveAnnouncementDndStarted: 'Dragging',
  liveAnnouncementDndDiscarded: 'Insertion discarded',
}`}},function(e){e.O(0,[81241,47439,81543,76075,46334,38517,53501,93241,60380,25205,12334,62256,99897,67036,12147,80543,27215,96286,42542,53309,15850,37804,90595,63561,91917,17773,74318,30628,93475,2315,4202,19164,62152,50590,71052,39145,30097,74736,95664,92086,73580,44645,83462,24159,58886,86310,68313,50865,12701,99236,58986,52269,96623,15935,43927,6377,21799,28666,80573,17015,54884,71093,11093,44570,61119,60103,63253,70718,63343,32108,54299,90425,58982,90975,15109,82277,87376,88616,5114,77343,19404,50294,48557,87639,60697,614,1438,54039,81293,1528,1744],function(){return e(e.s=57564)}),_N_E=e.O()}]);