import { useEffect, useState } from 'react';

export default function TableOfContents({ html }) {
  const [toc, setToc] = useState([]);
  
  useEffect(() => {
    if (typeof window !== 'undefined' && html) {
      // Create a temporary div to parse the HTML
      const div = document.createElement('div');
      div.innerHTML = html;
      
      // Find all headings (h2, h3, h4)
      const headings = Array.from(div.querySelectorAll('h2, h3, h4'));
      
      // Generate TOC
      const tocEntries = headings.map((heading, index) => {
        // Generate an ID if not present
        const id = heading.id || `heading-${index}`;
        
        // Set the ID in the heading (will be used for scroll)
        heading.id = id;
        
        return {
          id,
          text: heading.textContent,
          level: parseInt(heading.tagName.substring(1), 10),
        };
      });
      
      setToc(tocEntries);
    }
  }, [html]);
  
  if (toc.length === 0) return null;
  
  const scrollToHeading = (id) => {
    const element = document.getElementById(id);
    if (element) {
      // For smooth scrolling
      window.scrollTo({
        top: element.offsetTop - 100, // Offset for header
        behavior: 'smooth'
      });
    }
  };
  
  return (
    <div className="table-of-contents">
      <h4 className="mb-4 text-lg font-medium text-gray-900">Table of Contents</h4>
      <nav>
        <ul className="space-y-2 text-sm">
          {toc.map((item) => (
            <li 
              key={item.id}
              className={`cursor-pointer hover:text-blue-600 ${
                item.level === 2 ? 'font-medium' : 
                item.level === 3 ? 'ml-4' : 'ml-8'
              }`}
              onClick={() => scrollToHeading(item.id)}
            >
              {item.text}
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
