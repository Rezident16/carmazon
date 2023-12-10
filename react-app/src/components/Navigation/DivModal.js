import React from "react";
import { useModal } from "../../context/Modal";

function OpenModalDiv({
  modalComponent, // component to render inside the modal
  buttonText, // text of the button that opens the modal
  onButtonClick, // optional: callback function that will be called once the button that opens the modal is clicked
  onModalClose, // optional: callback function that will be called once the modal is closed
  className,
  divText,
}) {
  const { setModalContent, setOnModalClose } = useModal();
  const onClick = () => {
    if (onModalClose) setOnModalClose(onModalClose);
    setModalContent(modalComponent);
    if (onButtonClick) onButtonClick();
  };

  return (
    <div className={className} onClick={onClick}>
      {divText ? (<div className="modal_div_text">{divText}</div>) : (null)}
      <div>
        {buttonText}
      </div>
    </div>
  );
}

export default OpenModalDiv;
