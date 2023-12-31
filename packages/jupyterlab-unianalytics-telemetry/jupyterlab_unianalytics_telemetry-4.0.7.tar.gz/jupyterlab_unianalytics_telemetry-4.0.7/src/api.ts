import {
  BACKEND_API_URL,
  MAX_PAYLOAD_SIZE,
  POST_TOKEN
} from './utils/constants';
import {
  ICellAlterationObject,
  ICellClickObject,
  ICodeExecObject,
  INotebookClickObject,
  IMarkdownExecObject,
  PostDataObject
} from './utils/types';
import {
  enc as cryptoEnc,
  AES as cryptoAES,
  mode as cryptoMode
} from 'crypto-js';

const cryptoJSEncryption = (message: string): string => {
  // symmetric encryption
  const encrypted = cryptoAES.encrypt(
    message,
    cryptoEnc.Base64.parse('F0fbgrA8v9cqCHgzCgIOMou9CTYj5wTu'),
    {
      mode: cryptoMode.ECB
    }
  );

  return encrypted.toString();
};

const postRequest = (data: PostDataObject, endpoint: string): void => {
  const payload = JSON.stringify(data);
  const url = BACKEND_API_URL + endpoint;

  if (payload.length > MAX_PAYLOAD_SIZE) {
    console.log(
      `Payload size exceeds limit of ${MAX_PAYLOAD_SIZE / 1024 / 1024} Mb`
    );
    return;
  } else {
    console.log('Posting to ' + endpoint + ' :\n', data);
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // send encrypt([token, nonce]) as part of the header
        'Token-Auth': cryptoJSEncryption(
          JSON.stringify({ token: POST_TOKEN, nonce: crypto.randomUUID() })
        )
      },
      body: payload
    }).then(response => {
      response.json().then(responseData => console.log(responseData));
    });
  }
};

export const postCodeExec = (cellExec: ICodeExecObject): void => {
  postRequest(cellExec, 'exec/code');
};

export const postMarkdownExec = (markdownExec: IMarkdownExecObject): void => {
  postRequest(markdownExec, 'exec/markdown');
};

export const postCellClick = (cellClick: ICellClickObject): void => {
  postRequest(cellClick, 'clickevent/cell');
};

export const postNotebookClick = (
  notebookClick: INotebookClickObject
): void => {
  postRequest(notebookClick, 'clickevent/notebook');
};

export const postCellAlteration = (
  cellAlteration: ICellAlterationObject
): void => {
  postRequest(cellAlteration, 'alter');
};
