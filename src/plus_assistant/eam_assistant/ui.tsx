// src/plus_assistant/eam_assistant/ui.tsx

import React from 'react';

const WorkRequestComponent = (props: { requestId: string }) => {
  return <div>Work Request ID: {props.requestId}</div>;
};

export default {
  workRequest: WorkRequestComponent,
};