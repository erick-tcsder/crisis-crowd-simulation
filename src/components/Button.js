import classNames from 'classnames';

const iconPositions = {
  left: 'order-1 mr-3',
  right: 'order-3 ml-3',
};

export const Button = ({
  icon,
  iconPosition,
  className,
  ...buttonProps
}) => {

  return (
    <button
      disabled={buttonProps.loading}
      {...buttonProps}
      className={classNames(
        className,
        'flex justify-center items-center',
        {
          'p-2 px-3': !buttonProps.children,
        }
      )}
    >
      {buttonProps.children && (
        <span
          className={classNames({
            'order-2': icon,
          })}
        >
          {buttonProps.children}
        </span>
      )}
      {icon && (
        <i className={classNames({
          'hidden': !icon,
          'order-1 mr-2': !iconPosition && buttonProps.children,
          [`${iconPositions[iconPosition ?? 'left']}`]: iconPosition,
        },icon)}/>
      )}
    </button>
  );
};
