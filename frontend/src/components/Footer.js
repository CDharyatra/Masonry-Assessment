import React from 'react';

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="row">
          <div className="col-md-12 text-center">
            <p className="mb-0">© {new Date().getFullYear()} Web Research Agent - AI-powered research assistant</p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
