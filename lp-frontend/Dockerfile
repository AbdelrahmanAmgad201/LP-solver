# Development version
FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Use Vite's dev server instead of serve
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]