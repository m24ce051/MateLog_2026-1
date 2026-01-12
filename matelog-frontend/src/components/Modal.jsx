import { useEffect } from 'react';
import './Modal.css';

const Modal = ({
  isOpen,
  onClose,
  onConfirm,
  onCancel,
  title,
  message,
  type = 'info', // 'info', 'success', 'warning', 'error', 'confirm'
  confirmText = 'Aceptar',
  cancelText = 'Cancelar',
  showCancel = false
}) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
      case 'warning':
        return '!';
      case 'confirm':
        return '?';
      default:
        return 'i';
    }
  };

  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    }
    onClose();
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className={`modal-icon modal-icon-${type}`}>
          {getIcon()}
        </div>

        {title && <h3 className="modal-title">{title}</h3>}

        <div className="modal-message">{message}</div>

        <div className="modal-buttons">
          {showCancel && (
            <button onClick={handleCancel} className="modal-btn modal-btn-cancel">
              {cancelText}
            </button>
          )}
          <button onClick={handleConfirm} className="modal-btn modal-btn-confirm">
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
