
# Arabic Handwritten OCR

## Overview
This project is an Arabic Handwritten OCR (Optical Character Recognition) application built with React and Vite. It leverages various modern web technologies and libraries to provide a seamless user experience.

## Features
- **React**: A JavaScript library for building user interfaces.
- **Vite**: A build tool that provides a faster and leaner development experience for modern web projects.
- **Fast Refresh**: Enabled by either Babel or SWC for an improved development experience.
- **CSS Modules**: Scoped CSS to avoid conflicts.
- **Axios**: For making HTTP requests.
- **Framer Motion**: For animations.
- **React Icons**: For icons.
- **React Spinners**: For loading spinners.
- **SCSS**: For enhanced styling capabilities.
- **Tiff**: For handling TIFF image files.

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/arabic-handwritten-ocr.git
   cd arabic-handwritten-ocr
   ```

2. Install dependencies:
   ```sh
   npm install
   # or
   yarn install
   ```

### Running the Application
To start the development server:
```sh
npm run dev
# or
yarn dev
```
This will start the Vite development server and open the application in your default web browser.

### Building for Production
To build the application for production:
```sh
npm run build
# or
yarn build
```
The built files will be in the `dist` directory.

### Linting
To run ESLint:
```sh
npm run lint
# or
yarn lint
```

### Previewing the Production Build
To preview the production build:
```sh
npm run preview
# or
yarn preview
```

## Project Structure
```plaintext
├── Backend
│   ├── Backend_Debug.ipynb
├── src
│   ├── assets
│   │   └── TAAKWEEN_LOGO.svg
│   ├── Components
│   │   ├── Header
│   │   │   ├── Header.css
│   │   │   └── Header.jsx
│   │   ├── Modal
│   │   │   ├── Modal.css
│   │   │   └── Modal.jsx
│   │   ├── Results
│   │   │   ├── Results.css
│   │   │   ├── Results.css.map
│   │   │   └── Results.jsx
│   ├── App.css
│   ├── index.css
│   ├── main.jsx
├── index.html
├── package.json
├── README.md
├── vite.config.js
└── .gitignore
```

## Configuration
The Vite configuration is defined in `vite.config.js`:
```typescript:vite.config.js
startLine: 1
endLine: 23
```

## Dependencies
The project dependencies are listed in `package.json`:
```json:package.json
startLine: 12
endLine: 22
```

## Dev Dependencies
The development dependencies are listed in `package.json`:
```json:package.json
startLine: 23
endLine: 33
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [React](https://reactjs.org/)
- [Vite](https://vitejs.dev/)
- [Framer Motion](https://www.framer.com/motion/)
- [Axios](https://axios-http.com/)
- [React Icons](https://react-icons.github.io/react-icons/)
- [React Spinners](https://www.davidhu.io/react-spinners/)
- [SCSS](https://sass-lang.com/)
- [TIFF](https://www.libtiff.org/)

## Contact
For any inquiries or issues, please contact [your-email@example.com].
