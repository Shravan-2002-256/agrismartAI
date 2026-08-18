// Enhanced Export Component
// Export detection data in multiple formats
// PDF, CSV, JSON with customizable fields

import { FiDownload, FiX, FiFileText, FiFile } from 'react-icons/fi';
import { toast } from 'react-toastify';
import { useState } from 'react';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

const EnhancedExport = ({ isOpen, onClose, data, filename = 'agrismart-export' }) => {
  const [selectedFormat, setSelectedFormat] = useState('csv');
  const [includeFields, setIncludeFields] = useState({
    disease: true,
    confidence: true,
    cropType: true,
    severity: true,
    date: true,
    treatment: true,
    image: false
  });

  if (!isOpen) return null;

  const exportFormats = [
    { id: 'csv', name: 'CSV', icon: FiFileText, description: 'Spreadsheet format' },
    { id: 'json', name: 'JSON', icon: FiFile, description: 'Machine-readable' },
    { id: 'pdf', name: 'PDF', icon: FiFileText, description: 'Report format' }
  ];

  const handleExport = () => {
    if (!data || data.length === 0) {
      toast.error('No data to export');
      return;
    }

    try {
      switch (selectedFormat) {
        case 'csv':
          exportCSV();
          break;
        case 'json':
          exportJSON();
          break;
        case 'pdf':
          exportPDF();
          break;
      }
      toast.success(`Export successful: ${filename}.${selectedFormat}`);
      onClose();
    } catch (error) {
      console.error('Export error:', error);
      toast.error(`Export failed: ${error.message || 'Unknown error'}`);
    }
  };

  const exportCSV = () => {
    // Helper function to escape CSV values
    const escapeCSV = (value) => {
      if (!value && value !== 0) return '';
      const str = String(value);
      // Wrap in quotes if contains comma, newline, or quote
      if (str.includes(',') || str.includes('\n') || str.includes('"')) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };

    // Helper to capitalize first letter
    const capitalize = (str) => str ? str.charAt(0).toUpperCase() + str.slice(1) : '';

    const headers = [];
    if (includeFields.disease) headers.push('Disease');
    if (includeFields.confidence) headers.push('Confidence (%)');
    if (includeFields.cropType) headers.push('Crop Type');
    if (includeFields.severity) headers.push('Severity');
    if (includeFields.date) headers.push('Date & Time');
    if (includeFields.treatment) headers.push('Treatment Recommendation');

    const rows = data.map(item => {
      const row = [];
      
      if (includeFields.disease) {
        row.push(escapeCSV(item.disease_detected || 'Unknown'));
      }
      
      if (includeFields.confidence) {
        const confidence = item.confidence ? Math.round(item.confidence) : 0;
        row.push(confidence);
      }
      
      if (includeFields.cropType) {
        row.push(escapeCSV(capitalize(item.crop_type || 'Unknown')));
      }
      
      if (includeFields.severity) {
        row.push(escapeCSV(capitalize(item.severity || 'none')));
      }
      
      if (includeFields.date) {
        const date = new Date(item.detected_at);
        const formatted = date.toLocaleString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
        row.push(escapeCSV(formatted));
      }
      
      if (includeFields.treatment) {
        // Try multiple possible field names for treatment
        const treatment = item.treatment_recommended || 
                         item.treatment || 
                         item.recommendations ||
                         (item.severity === 'none' || item.severity === 'low' 
                           ? 'Monitor regularly, maintain good practices' 
                           : 'Consult with agronomist for specific treatment');
        row.push(escapeCSV(treatment));
      }
      
      return row.join(',');
    });

    const csv = [headers.join(','), ...rows].join('\n');
    downloadFile(csv, `${filename}.csv`, 'text/csv');
  };

  const exportJSON = () => {
    const capitalize = (str) => str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
    
    const filteredData = data.map(item => {
      const filtered = {};
      
      if (includeFields.disease) {
        filtered.disease = item.disease_detected || 'Unknown';
      }
      
      if (includeFields.confidence) {
        filtered.confidence = item.confidence ? `${Math.round(item.confidence)}%` : '0%';
      }
      
      if (includeFields.cropType) {
        filtered.cropType = capitalize(item.crop_type || 'Unknown');
      }
      
      if (includeFields.severity) {
        filtered.severity = capitalize(item.severity || 'none');
      }
      
      if (includeFields.date) {
        filtered.date = item.detected_at;
        filtered.formattedDate = new Date(item.detected_at).toLocaleString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      }
      
      if (includeFields.treatment) {
        const treatment = item.treatment_recommended || 
                         item.treatment || 
                         item.recommendations ||
                         (item.severity === 'none' || item.severity === 'low' 
                           ? 'Monitor regularly, maintain good practices' 
                           : 'Consult with agronomist for specific treatment');
        filtered.treatment = treatment;
      }
      
      if (includeFields.image) {
        filtered.imageUrl = item.image_url;
      }
      
      return filtered;
    });

    const json = JSON.stringify(filteredData, null, 2);
    downloadFile(json, `${filename}.json`, 'application/json');
  };

  const exportPDF = () => {
    const capitalize = (str) => str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
    
    // Create new PDF document
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    
    // Header - AgriSmart Branding
    doc.setFillColor(16, 185, 129); // Primary green color
    doc.rect(0, 0, pageWidth, 35, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(24);
    doc.setFont(undefined, 'bold');
    doc.text('AgriSmart', 14, 15);
    
    doc.setFontSize(12);
    doc.setFont(undefined, 'normal');
    doc.text('Disease Detection History Report', 14, 25);
    
    // Export timestamp
    const exportDate = new Date().toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
    doc.setFontSize(9);
    doc.text(`Generated: ${exportDate}`, pageWidth - 14, 15, { align: 'right' });
    doc.text(`Total Records: ${data.length}`, pageWidth - 14, 22, { align: 'right' });
    
    // Reset text color for body
    doc.setTextColor(0, 0, 0);
    
    // Summary Statistics
    let yPos = 45;
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('Summary Statistics', 14, yPos);
    
    yPos += 8;
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    
    // Calculate statistics
    const stats = {
      total: data.length,
      highSeverity: data.filter(d => d.severity === 'high').length,
      diseases: [...new Set(data.map(d => d.disease_detected))].length,
      avgConfidence: Math.round(data.reduce((sum, d) => sum + (d.confidence || 0), 0) / data.length)
    };
    
    const statsText = [
      `Total Detections: ${stats.total}`,
      `High Severity Cases: ${stats.highSeverity}`,
      `Unique Diseases: ${stats.diseases}`,
      `Average Confidence: ${stats.avgConfidence}%`
    ];
    
    statsText.forEach((text, i) => {
      doc.text(`• ${text}`, 20, yPos + (i * 6));
    });
    
    yPos += 30;
    
    // Prepare table data
    const tableColumns = [];
    const columnHeaders = [];
    
    if (includeFields.disease) {
      tableColumns.push('disease');
      columnHeaders.push('Disease');
    }
    if (includeFields.confidence) {
      tableColumns.push('confidence');
      columnHeaders.push('Confidence');
    }
    if (includeFields.cropType) {
      tableColumns.push('cropType');
      columnHeaders.push('Crop');
    }
    if (includeFields.severity) {
      tableColumns.push('severity');
      columnHeaders.push('Severity');
    }
    if (includeFields.date) {
      tableColumns.push('date');
      columnHeaders.push('Date');
    }
    if (includeFields.treatment) {
      tableColumns.push('treatment');
      columnHeaders.push('Treatment');
    }
    
    const tableRows = data.map(item => {
      const row = [];
      
      if (includeFields.disease) {
        row.push(item.disease_detected || 'Unknown');
      }
      if (includeFields.confidence) {
        row.push(`${Math.round(item.confidence || 0)}%`);
      }
      if (includeFields.cropType) {
        row.push(capitalize(item.crop_type || 'Unknown'));
      }
      if (includeFields.severity) {
        row.push(capitalize(item.severity || 'none'));
      }
      if (includeFields.date) {
        const date = new Date(item.detected_at);
        row.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }));
      }
      if (includeFields.treatment) {
        const treatment = item.treatment_recommended || 
                         item.treatment || 
                         (item.severity === 'none' || item.severity === 'low' 
                           ? 'Monitor regularly' 
                           : 'Consult agronomist');
        row.push(treatment);
      }
      
      return row;
    });
    
    // Generate table with autoTable
    doc.autoTable({
      head: [columnHeaders],
      body: tableRows,
      startY: yPos,
      theme: 'grid',
      headStyles: {
        fillColor: [16, 185, 129],
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        halign: 'center'
      },
      styles: {
        fontSize: 9,
        cellPadding: 3,
        overflow: 'linebreak',
        halign: 'left'
      },
      columnStyles: {
        0: { cellWidth: 'auto' },
        1: { halign: 'center', cellWidth: 20 },
        2: { halign: 'center', cellWidth: 20 },
        3: { halign: 'center', cellWidth: 20 },
        4: { cellWidth: 25 },
        5: { cellWidth: 'auto' }
      },
      alternateRowStyles: {
        fillColor: [245, 247, 250]
      },
      margin: { top: 10, left: 14, right: 14 },
      didDrawPage: (data) => {
        // Footer with page numbers
        const pageCount = doc.internal.getNumberOfPages();
        doc.setFontSize(8);
        doc.setTextColor(128);
        
        for (let i = 1; i <= pageCount; i++) {
          doc.setPage(i);
          doc.text(
            `Page ${i} of ${pageCount}`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
          );
          doc.text(
            'AgriSmart © 2026',
            14,
            pageHeight - 10
          );
        }
      }
    });
    
    // Save PDF
    doc.save(`${filename}.pdf`);
  };

  const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-lg w-full">
        {/* Header */}
        <div className="border-b border-gray-200 dark:border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <FiDownload className="text-primary-600 dark:text-primary-400 text-xl" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">Export Data</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {data?.length || 0} detection{data?.length !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
            <FiX className="text-gray-600 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Format Selection */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-3">
              Export Format
            </label>
            <div className="grid grid-cols-3 gap-3">
              {exportFormats.map(format => (
                <button
                  key={format.id}
                  onClick={() => setSelectedFormat(format.id)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    selectedFormat === format.id
                      ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20'
                      : 'border-gray-200 dark:border-gray-600 hover:border-primary-400'
                  }`}
                >
                  <format.icon className="mx-auto text-2xl mb-2 text-gray-700 dark:text-gray-300" />
                  <p className="font-semibold text-sm text-gray-900 dark:text-white">{format.name}</p>
                  <p className="text-xs text-gray-500">{format.description}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Field Selection */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-3">
              Include Fields
            </label>
            <div className="space-y-2">
              {Object.entries(includeFields).map(([field, checked]) => {
                // User-friendly field labels
                const fieldLabels = {
                  disease: 'Disease Name',
                  confidence: 'Confidence Score',
                  cropType: 'Crop Type',
                  severity: 'Severity Level',
                  date: 'Detection Date & Time',
                  treatment: 'Treatment Recommendations',
                  image: 'Image URL'
                };
                
                return (
                  <label key={field} className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={checked}
                      onChange={(e) => setIncludeFields(prev => ({ ...prev, [field]: e.target.checked }))}
                      className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-900 dark:text-white">
                      {fieldLabels[field] || field}
                    </span>
                  </label>
                );
              })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-6 flex gap-3">
          <button onClick={onClose} className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-medium">
            Cancel
          </button>
          <button onClick={handleExport} className="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium flex items-center justify-center gap-2">
            <FiDownload />
            Export
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedExport;
