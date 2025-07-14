import { createInterface } from 'readline';

export function createReadline() {
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return {
    question: (query) => {
      return new Promise((resolve) => {
        rl.question(query, resolve);
      });
    },
    close: () => {
      rl.close();
    }
  };
}